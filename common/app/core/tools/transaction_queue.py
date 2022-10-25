from PyQt5.Qt import QObject, pyqtSignal
from logging import info
from collections import deque
from common.app.core.tools.parser import Parser
from common.app.data_models.message import Message
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.data_models.config import Config
from common.app.core.tools.fields_generator import FieldsGenerator
from common.app.data_models.transaction import Transaction


class TransactionQueue(QObject):
    _queue: deque = deque(maxlen=1024)
    _transactions_count: int = int()
    _transaction_accepted: pyqtSignal = pyqtSignal(str)
    _message_ready_to_send: pyqtSignal = pyqtSignal()
    _spec: EpaySpecification = EpaySpecification()
    _send_message: pyqtSignal = pyqtSignal(Message)

    @property
    def send_message(self):
        return self._send_message

    @property
    def spec(self):
        return self._spec

    @property
    def transaction_accepted(self):
        return self._transaction_accepted

    @property
    def transaction_count(self):
        return self._transactions_count

    @transaction_count.setter
    def transaction_count(self, transaction_count):
        self._transactions_count = transaction_count

    def __init__(self, config: Config):
        QObject.__init__(self)
        self.config: Config = config
        self.parser: Parser = Parser(self.config)

    def put_transaction(self, transaction: Transaction) -> None:
        if not transaction.trans_id:
            transaction.trans_id = FieldsGenerator.trans_id()

        self._queue.append(transaction)

    def get_reversible_transactions(self) -> list[Message]:
        transactions: list[Message] = []

        transaction: Transaction

        for transaction in self._queue:
            if not self.spec.get_reversal_mti(transaction.request.transaction.message_type):
                continue

            transactions.append(transaction.request)

        return transactions

    def get_last_reversible_transaction_id(self) -> str:
        if reversible := self.get_reversible_transactions():
            return max(message.transaction.id for message in reversible)

    def remove_from_queue(self, transaction):
        self._queue.remove(transaction)

    def get_transaction(self, trans_id) -> Transaction | None:
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
            return  False

        matched_request.matched = True
        response.matched = True
        response.match_id = matched_request.trans_id
        matched_request.match_id = response.trans_id
        return True

    def put_response(self, response: Transaction):
        if not response.trans_id:
            response.trans_id = FieldsGenerator.trans_id()

        self._queue.append(response)

        if not self.match_transaction(response):
            return

        resp_time = 3 # round(transaction.timer.total_seconds(), 3)
        info(f"Transaction ID [{response.match_id}] matched. Response time seconds: {resp_time}")

    # def start_transaction_timer(self, request: Message):
    #     if not (transaction := self.get_transaction(request.transaction.id)):
    #         return
    #
    #     transaction.start_timer()
