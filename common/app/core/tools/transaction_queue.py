from PyQt5.Qt import QObject, pyqtSignal
from typing import Optional
from logging import info
from collections import deque
from common.app.core.tools.transaction import Transaction
from common.app.core.tools.parser import Parser
from common.app.data_models.message import Message
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.data_models.config import Config
from common.app.core.tools.fields_generator import FieldsGenerator


class TransactionQueue(QObject):
    _queue: deque = deque(maxlen=1024)
    _transactions_count: int = int()
    _transaction_accepted: pyqtSignal = pyqtSignal(str)
    _message_ready_to_send: pyqtSignal = pyqtSignal()
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    @property
    def transaction_accepted(self):
        return self._transaction_accepted

    @property
    def queue(self):
        return self._queue

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

    def create_transaction(self, message: Message) -> None:
        if not message.transaction.id:
            message.transaction.id = FieldsGenerator.trans_id()

        self.queue.append(Transaction(request=message, trans_id=message.transaction.id))

    def get_reversible_transactions(self) -> list[Transaction]:
        return [
            trans for trans in self.queue
            if trans.request.transaction.message_type in self.spec.reversible_messages
        ]

    def get_last_reversible_transaction_id(self) -> str:
        if reversible := self.get_reversible_transactions():
            return max(trans.trans_id for trans in reversible)

    def remove_from_queue(self, transaction):
        self.queue.remove(transaction)

    def get_transaction(self, trans_id) -> Transaction | None:
        transaction = None

        for trans in self.queue:
            if trans_id == trans.trans_id:
                transaction = trans
                break

        return transaction

    def put_response_message(self, response: Message):
        transaction: Transaction

        for transaction in self.queue:
            if not transaction.match(request=transaction.request, response=response):
                continue

            resp_time = round(transaction.timer.total_seconds(), 3)
            info(f"Transaction ID [{transaction.trans_id}] matched. Response time seconds: {resp_time}")
            transaction.put_response(response)

            return
