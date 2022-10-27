from PyQt5.Qt import QObject, pyqtSignal
from collections import deque
from common.app.core.tools.parser import Parser
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.data_models.config import Config
from common.app.core.tools.fields_generator import FieldsGenerator
from common.app.data_models.transaction import Transaction
from common.app.core.tools.transaction_timer import TransactionTimer


class TransactionQueue(QObject):
    _spec: EpaySpecification = EpaySpecification()
    _queue: deque = deque(maxlen=1024)
    _transaction_matched: pyqtSignal = pyqtSignal(str, float)

    @property
    def spec(self):
        return self._spec

    @property
    def transaction_matched(self):
        return self._transaction_matched

    def __init__(self, config: Config):
        QObject.__init__(self)
        self.config: Config = config
        self.parser: Parser = Parser(self.config)

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

    def put_transaction(self, transaction: Transaction) -> None:
        if self.is_request(transaction):
            self._queue.append(transaction)
            return

        if not transaction.trans_id:
            transaction.trans_id = FieldsGenerator.trans_id()

        if not self.match_transaction(transaction):
            return

        self.transaction_matched.emit(transaction.match_id, 0.568)

    def is_request(self, transaction: Transaction) -> bool:
        if not transaction.message_type in self.spec.get_mti_codes():
            raise ValueError(f"Incorrect MTI {transaction.message_type}")

        for mti in self.spec.mti:
            if transaction.message_type == mti.request:
                return True

        return False
