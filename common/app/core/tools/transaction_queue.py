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
    _transaction_matched: pyqtSignal = pyqtSignal(Transaction, float)
    _incoming_transaction: pyqtSignal = pyqtSignal(Transaction)
    _outgoing_transaction: pyqtSignal = pyqtSignal(Transaction)
    _resp_received: pyqtSignal = pyqtSignal(Transaction)

    @property
    def spec(self):
        return self._spec

    @property
    def transaction_matched(self):
        return self._transaction_matched

    @property
    def incoming_transaction(self):
        return self._incoming_transaction

    def __init__(self, config: Config, connector: ConnectionWorker):
        QObject.__init__(self)
        self.config: Config = config
        self.connector: ConnectionWorker = connector
        self.parser: Parser = Parser(self.config)
        self.timers: dict[str, QTimer] = {}
        self._start_connection_thread()

    def _start_connection_thread(self):
        self._connection_thread: QThread = QThread()
        self.connector.moveToThread(self._connection_thread)
        self._outgoing_transaction.connect(self.connector.send_transaction)
        self._connection_thread.started.connect(self.connector.run)
        self.connector.ready_read.connect(self.read_from_socket)
        self.connector.transaction_sent.connect(self.start_transaction_timer)
        self._resp_received.connect(self.stop_transaction_timer)
        self._connection_thread.start()

    def start_transaction_timer(self, transaction: Transaction, timeout=60):
        if not (timer := self.timers.get(transaction.trans_id)):
            timer: QTimer = QTimer()

        self.timers[transaction.trans_id] = timer
        timer.timeout.connect(lambda: self.process_timeout(transaction))
        timer.start(timeout * 1000)

    def stop_transaction_timer(self, transaction):
        timer: QTimer

        if not (timer := self.timers.get(transaction.trans_id)):
            return

        if not timer.isActive():
            return

        time_spend = (timer.interval() - timer.remainingTime()) / 1000
        self.transaction_matched.emit(transaction, time_spend)
        timer.stop()

    def read_from_socket(self):
        data = self.connector.read_from_socket().data()

        try:
            transaction: Transaction = self.parser.parse_dump(data=data)
        except Exception as parsing_error:
            error("Incoming transaction parsing error: %s", parsing_error)
            return

        self.put_transaction(transaction)
        self.incoming_transaction.emit(transaction)

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

    def process_timeout(self, transaction):
        timer: QTimer

        if not (timer := self.timers.get(transaction.trans_id)):
            return

        timeout_secs = int(timer.interval() / 1000)
        error(f"Transaction [{transaction.trans_id}] got SV timeout after {timeout_secs} seconds of waiting")
        timer.stop()

    def put_transaction(self, transaction: Transaction) -> None:
        timer: QTimer

        if self.is_request(transaction):
            self._outgoing_transaction.emit(transaction)
            self._queue.append(transaction)
            timer = QTimer()
            self.timers[transaction.trans_id] = timer
            return

        if not transaction.trans_id:
            transaction.trans_id = FieldsGenerator.trans_id()

        self._queue.append(transaction)

        if not self.match_transaction(transaction):
            warning(f"Received unmatched response [{transaction.trans_id}]")
            return

        self._resp_received.emit(self.get_transaction(transaction.match_id))

    def is_request(self, transaction: Transaction) -> bool:
        if transaction.message_type not in self.spec.get_mti_codes():
            raise ValueError(f"Incorrect MTI {transaction.message_type}")

        for mti in self.spec.mti:
            if transaction.message_type == mti.request:
                return True

        return False
