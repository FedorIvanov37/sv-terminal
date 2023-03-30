from collections import deque
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtCore import QTimer
from .EpaySpecification import EpaySpecification
from .FieldsGenerator import FieldsGenerator
from .data_models.Transaction import Transaction
from common.gui.core.connection_worker import ConnectionWorker
from common.lib.data_models.Config import Config


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

    @property
    def connector(self):
        return self._connector

    def __init__(self, config: Config):
        QObject.__init__(self)
        self.config = config
        self._connector = ConnectionWorker(self.config)
        self.generator: FieldsGenerator = FieldsGenerator()
        self.timers: dict[str, QTimer] = {}
        self._start_connection_thread()

    def _start_connection_thread(self):
        self._connection_thread: QThread = QThread()
        self.connector.moveToThread(self._connection_thread)
        self._ready_to_send.connect(self.connector.send_transaction)
        self._connection_thread.started.connect(self.connector.run)
        self.connector.transaction_received.connect(self.put_transaction)
        self.connector.transaction_sent.connect(self.request_was_sent)
        self._connection_thread.start()

    def put_transaction(self, transaction):
        transaction.is_request = self.spec.is_request(transaction)
        self._queue.append(transaction)

        if transaction.is_request:
            self._put_request(transaction)
            return

        self._put_response(transaction)

    def _put_request(self, request: Transaction):
        if not request.is_request:
            raise TypeError("Wrong MTI")

        self._ready_to_send.emit(request)

    def _put_response(self, response: Transaction):
        if response.is_request:
            raise TypeError("Wrong MTI")

        if self.match_transaction(response):
            response.resp_time_seconds = self.stop_transaction_timer(response)
            request = self.get_transaction(response.match_id)
            self.generator.merge_trans_data(request, response)

        if not response.trans_id:
            response.trans_id = self.generator.trans_id()

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

    def get_last_reversible_transaction_id(self) -> str:
        if reversible_transactions := self.get_reversible_transactions():
            return max(transaction.trans_id for transaction in reversible_transactions)

    def get_reversible_transactions(self) -> list[Transaction]:
        transactions: list[Transaction] = []

        transaction: Transaction

        for transaction in self._queue:
            if not self.spec.get_reversal_mti(transaction.message_type):
                continue

            transactions.append(transaction)

        return transactions

    def remove_from_queue(self, transaction):
        transactions_to_remove = [
            trans for trans in self._queue if transaction.trans_id in (trans.trans_id, trans.match_id)
        ]

        for transaction in transactions_to_remove:
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
