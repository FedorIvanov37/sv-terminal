from logging import error, warning
from collections import deque
from PyQt5.Qt import QObject, pyqtSignal, QThread
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.core.tools.fields_generator import FieldsGenerator
from common.app.data_models.config import Config
from common.app.core.tools.parser import Parser
from common.app.core.tools.connector import ConnectionWorker
from common.app.data_models.transaction import Transaction
from PyQt5.QtCore import QTimer


class TransactionQueue(QObject):
    _spec: EpaySpecification = EpaySpecification()
    _queue: deque[Transaction] = deque(maxlen=1024)
    _incoming_transaction: pyqtSignal = pyqtSignal(Transaction)
    _outgoing_transaction: pyqtSignal = pyqtSignal(Transaction)
    _transaction_timeout: pyqtSignal = pyqtSignal(Transaction, float)
    _ready_to_send: pyqtSignal = pyqtSignal(Transaction)

    @property
    def spec(self):
        return self._spec

    @property
    def incoming_transaction(self):
        return self._incoming_transaction

    @property
    def outgoing_transaction(self):
        return self._outgoing_transaction

    @property
    def transaction_timeout(self):
        return self._transaction_timeout

    def __init__(self, config: Config, connector: ConnectionWorker):
        QObject.__init__(self)
        self.config: Config = config
        self.connector: ConnectionWorker = connector
        self.parser: Parser = Parser(self.config)
        self.generator: FieldsGenerator = FieldsGenerator(self.config)
        self.timers: dict[str, QTimer] = {}
        self._start_connection_thread()

    def _start_connection_thread(self):
        self._connection_thread: QThread = QThread()
        self.connector.moveToThread(self._connection_thread)
        self._ready_to_send.connect(self.connector.send_transaction)
        self._connection_thread.started.connect(self.connector.run)
        self.connector.ready_read.connect(self.read_from_socket)
        self.connector.transaction_sent.connect(self.request_was_sent)
        self._connection_thread.start()

    def put_request(self, request: Transaction):
        request.is_request = self.spec.is_request(request)

        if not request.is_request:
            raise TypeError("Fatal error: Trying to parse transaction request as a response")

        self._queue.append(request)
        self._ready_to_send.emit(request)

    def put_response(self, response: Transaction):
        response.is_request = self.spec.is_request(response)

        if response.is_request:
            raise TypeError("Fatal error: Trying to parse transaction response as a request")

        self._queue.append(response)

        if self.match_transaction(response):
            response.resp_time_seconds = self.stop_transaction_timer(response)
            request = self.get_transaction(response.match_id)
            self.generator.merge_trans_data(request, response)

        if not response.trans_id:
            response.trans_id = FieldsGenerator.trans_id()

        self.incoming_transaction.emit(response)

    def start_transaction_timer(self, transaction: Transaction, timeout=60):
        timer: QTimer = QTimer()
        timer.timeout.connect(lambda: self.process_timeout(transaction))
        self.timers[transaction.trans_id] = timer
        timer.start(timeout * 1000)

    def stop_transaction_timer(self, response):
        timer: QTimer

        if not (timer := self.timers.get(response.match_id)):
            return

        if not timer.isActive():
            return

        time_spend = (timer.interval() - timer.remainingTime()) / 1000
        timer.stop()
        return time_spend

    def process_timeout(self, transaction):
        timer: QTimer

        if not (timer := self.timers.get(transaction.trans_id)):
            return

        timeout_secs = int(timer.interval() / 1000)
        self.transaction_timeout.emit(transaction, timeout_secs)
        timer.stop()

    def request_was_sent(self, request):
        self.start_transaction_timer(request)
        self.outgoing_transaction.emit(request)

    def read_from_socket(self):
        data = self.connector.read_from_socket().data()

        try:
            response: Transaction = self.parser.parse_dump(data=data)
        except Exception as parsing_error:
            error("Incoming transaction parsing error: %s", parsing_error)
            return

        self.put_response(response)

    def get_reversible_transactions(self) -> list[Transaction]:
        transactions: list[Transaction] = []

        transaction: Transaction

        for transaction in self._queue:
            if not self.spec.get_reversal_mti(transaction.message_type):
                continue

            transactions.append(transaction)

        return transactions

    def get_last_reversible_transaction_id(self) -> str:
        if reversible_transactions := self.get_reversible_transactions():
            return max(transaction.trans_id for transaction in reversible_transactions)

    def remove_from_queue(self, transaction):
        self._queue.remove(transaction)

    def get_transaction(self, trans_id: str) -> Transaction | None:
        transaction = None

        for trans in self._queue:
            if trans_id == trans.trans_id:
                transaction = trans
                break

        return transaction

    def is_matched(self, request: Transaction, response: Transaction) -> bool:
        if request.matched or response.matched:
            return False

        if response.message_type != self.spec.get_resp_mti(request.message_type):
            return False

        for field in self.spec.get_match_fields():
            if request.data_fields.get(field) != response.data_fields.get(field):
                return False

        return True

    def match_transaction(self, response: Transaction) -> bool:
        matched_request: Transaction | None = None

        for request in self._queue:
            if not self.is_matched(request, response):
                continue

            matched_request = request

        if not matched_request:
            return False

        matched_request.matched = True
        response.matched = True
        response.match_id = matched_request.trans_id
        matched_request.match_id = response.trans_id
        return True

    def is_request(self, transaction: Transaction) -> bool:
        if transaction.message_type not in self.spec.get_mti_codes():
            raise ValueError(f"Incorrect MTI {transaction.message_type}")

        for mti in self.spec.mti:
            if transaction.message_type == mti.request:
                return True

        return False
