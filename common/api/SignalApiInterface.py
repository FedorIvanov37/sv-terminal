from PyQt6.QtCore import QObject, pyqtSignal, QThread, QCoreApplication
from logging import error
from common.lib.data_models.Transaction import Transaction
from common.lib.core.Parser import Parser
from common.lib.core.EpaySpecification import EpaySpecification
from common.api.SignalApi import SignalApi
from common.lib.core.TransactionQueue import TransactionQueue


class SignalApiInterface(QObject):
    stop: bool = False

    _got_message: pyqtSignal = pyqtSignal(str, str)
    _transaction: pyqtSignal = pyqtSignal(Transaction)
    _incoming_transaction: pyqtSignal(Transaction)
    _spec: EpaySpecification = EpaySpecification()
    _run_api: pyqtSignal = pyqtSignal()

    @property
    def incoming_transaction(self):
        return self._incoming_transaction

    @property
    def got_message(self):
        return self._got_message

    @property
    def got_transaction(self):
        return self._transaction

    @property
    def run_api(self):
        return self._run_api

    def __init__(self):
        super().__init__()
        self.api = SignalApi()
        self.thread = QThread()
        self.api.moveToThread(self.thread)
        self._run_api.connect(self.api.run)
        self.thread.started.connect(self.run)
        self.thread.start()

    def run(self):
        while not self.stop:  # Main endless cycle
            QCoreApplication.processEvents()  # Processes events instead of direct interaction
            QThread.msleep(10)

        self.thread.terminate()

    def stop_thread(self):  # Once the self.stop become True the thread will be terminated
        self.stop = True

    def get_transaction(self, trans_id: str) -> Transaction:
        transaction: Transaction = self.trans_queue.get_transaction(trans_id)

        for field, field_data in transaction.data_fields.items():
            if not self._spec.is_field_complex([field]):
                continue

            try:
                transaction.data_fields[field] = Parser.split_complex_field(field, field_data)
            except Exception as parsing_error:
                error(parsing_error)
                continue

        return transaction
