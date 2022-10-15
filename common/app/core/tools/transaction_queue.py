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
    _queue: deque = deque(maxlen=512)
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

    def create_transaction(self, request: Message) -> Transaction:
        if not request.transaction.id:
            request.transaction.id = FieldsGenerator.trans_id()

        transaction: Transaction = Transaction(request=request, trans_id=request.transaction.id)
        self.queue.append(transaction)
        return transaction

    def get_reversible_transactions(self) -> list[Transaction]:
        return [
            trans for trans in self.queue
            if trans.request.transaction.message_type_indicator in self.spec.reversible_messages
        ]

    def get_last_transaction(self, reversible: Optional[bool] = False) -> Optional[Transaction]:
        if not reversible:
            id_list = self.queue

        else:
            id_list: list[str] | tuple | deque = list()

            for trans in self.queue:
                mti = trans.request.transaction.message_type_indicator

                if not self.spec.is_reversible(mti):
                    continue

                id_list.append(trans.trans_id)

        return self.get_transaction(trans_id=max(id_list))

    def remove_from_queue(self, transaction):
        self.queue.remove(transaction)

    def get_transaction(self, trans_id: str = None, reversible: Optional[bool] = False) -> Optional[Transaction]:
        transaction = None

        if trans_id is None:
            return self.get_last_transaction(reversible=reversible)

        for trans in self.queue:
            if trans.trans_id == trans_id:
                transaction = trans
                break

        if transaction is None:
            return

        is_reversible = self.spec.is_reversible(transaction.request.transaction.message_type_indicator)

        if reversible and not is_reversible:
            return

        return transaction

    def put_response(self, response: Message):
        for transaction in self.queue:
            if transaction.match(response=response):
                resp_time = round(transaction.timer.total_seconds(), 3)
                info("Transaction ID [%s] matched. Response time seconds: %s ", transaction.trans_id, resp_time)
                response.transaction.id = transaction.trans_id
                transaction.put_response(response)
                return transaction.trans_id
