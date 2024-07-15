from PyQt6.QtCore import QObject, pyqtSignal, QThread, QCoreApplication
from common.lib.data_models.Transaction import Transaction
from common.lib.core.EpaySpecification import EpaySpecification
from common.api.SignalApi import SignalApi
from common.lib.data_models.Config import Config
from os import getpid
from common.lib.core.LogStream import LogStream


class SignalApiInterface(QObject):
    stop: bool = False

    _got_message: pyqtSignal = pyqtSignal(str, str)
    _transaction: pyqtSignal = pyqtSignal(Transaction)
    _incoming_transaction: pyqtSignal = pyqtSignal(Transaction)
    _spec: EpaySpecification = EpaySpecification()
    _run_api: pyqtSignal = pyqtSignal()

    @property
    def pid(self):
        return getpid()

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

    def __init__(self, config: Config, terminal):
        super().__init__()
        self.log_stream = LogStream(terminal.window.log_browser)
        self.api = SignalApi(self.log_stream)
        self.thread = QThread()
        self.api.moveToThread(self.thread)
        self.api.connector.config = config
        self.api.connector.trans_queue = terminal.trans_queue
        self.api.connector.terminal = terminal
        self.api.connector.tcp_connector = terminal.connector
        self.api.connector.incoming_transaction.connect(self.incoming_transaction)
        self.run_api.connect(self.api.run)
        self.thread.started.connect(self.run)
        self.thread.start()

    def run(self):
        while not self.stop:  # Main endless cycle
            QCoreApplication.processEvents()  # Processes events instead of direct interaction
            QThread.msleep(10)

        self.thread.terminate()

        try:
            self.api.stop_api()
        except KeyboardInterrupt:
            return

    def stop_thread(self):  # Once the self.stop become True the thread will be terminated
        self.stop = True
