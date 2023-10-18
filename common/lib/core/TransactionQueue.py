from logging import error
from collections import deque
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QTimer
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.core.FieldsGenerator import FieldsGenerator
from common.lib.data_models.Transaction import Transaction
from common.lib.core.Parser import Parser
from common.lib.interfaces.ConnectorInterface import ConnectionInterface


class TransactionQueue(QObject):
    spec: EpaySpecification = EpaySpecification()
    queue: deque[Transaction] = deque(maxlen=1024)
    incoming_transaction: pyqtSignal = pyqtSignal(Transaction)
    outgoing_transaction: pyqtSignal = pyqtSignal(Transaction)
    transaction_timeout: pyqtSignal = pyqtSignal(Transaction, float)
    ready_to_send: pyqtSignal = pyqtSignal(str, bytes)

    def __init__(self, connector: ConnectionInterface):
        QObject.__init__(self)
        self.connector = connector
        self.generator: FieldsGenerator = FieldsGenerator()
        self.timers: dict[str, QTimer] = {}
        self.ready_to_send.connect(self.connector.send_transaction_data)
        self.connector.incoming_transaction_data.connect(self.receive_transaction_data)
        self.connector.transaction_sent.connect(self.request_was_sent)

    def send_transaction_data(self, request: Transaction):
        if not request.is_request:
            raise TypeError("Wrong MTI")

        try:
            transaction_dump: bytes = Parser.create_dump(request)
        except ValueError | TypeError as parsing_error:
            error(f"Parsing error: {parsing_error}")
            return

        self.ready_to_send.emit(request.trans_id, transaction_dump)

    def receive_transaction_data(self, transaction_data: bytes):
        try:
            transaction: Transaction = Parser.parse_dump(transaction_data)

        except Exception as parsing_error:
            error(f"Incoming transaction parsing error: {parsing_error}")

        else:
            self.put_transaction(transaction)

    def put_transaction(self, transaction, send=True):
        transaction.is_request = self.spec.is_request(transaction)
        self.queue.append(transaction)

        if send and transaction.is_request:
            self.send_transaction_data(transaction)
            return

        self.put_response(transaction)

    def put_response(self, response: Transaction):
        if response.is_request:
            raise TypeError("Wrong MTI")

        if self.match_transaction(response):
            response.resp_time_seconds = self.stop_transaction_timer(response)
            request = self.get_transaction(response.match_id)
            self.generator.merge_trans_data(request, response)

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

    def request_was_sent(self, trans_id):
        if not (request := self.get_transaction(trans_id)):
            return

        self.start_transaction_timer(request)
        self.outgoing_transaction.emit(request)

    def get_last_reversible_transaction_id(self) -> str:
        if reversible_transactions := self.get_reversible_transactions():
            return max(transaction.trans_id for transaction in reversible_transactions)

    def get_reversible_transactions(self) -> list[Transaction]:
        transactions: list[Transaction] = []

        transaction: Transaction

        for transaction in self.queue:
            if not self.spec.get_reversal_mti(transaction.message_type):
                continue

            transactions.append(transaction)

        return transactions

    def remove_from_queue(self, transaction):
        transactions_to_remove = [
            trans for trans in self.queue if transaction.trans_id in (trans.trans_id, trans.match_id)
        ]

        for transaction in transactions_to_remove:
            self.queue.remove(transaction)

    def get_transaction(self, trans_id: str) -> Transaction | None:
        transaction = None

        for trans in self.queue:
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

        for request in self.queue:
            if not self.is_matched(request, response):
                continue

            matched_request = request
            break

        if not matched_request:
            return False

        matched_request.matched = True
        response.matched = True
        response.match_id = matched_request.trans_id
        matched_request.match_id = response.trans_id

        return True
