from common.lib.core.Connector import Connector
from common.lib.data_models.Config import Config
from PyQt6.QtCore import QObject, QThread, QCoreApplication


class ConnectionThread(QObject):
    thread: QThread
    stop: bool = False

    @property
    def connected(self):
        return self.connector.connected

    @property
    def disconnected(self):
        return self.connector.disconnected

    @property
    def state(self):
        return self.connector.state

    @property
    def error(self):
        return self.connector.error

    @property
    def errorString(self):
        return self.connector.errorString

    @property
    def errorOccurred(self):
        return self.connector.errorOccurred

    @property
    def connect_sv(self):
        return self.connector.connect_sv

    @property
    def disconnect_sv(self):
        return self.connector.disconnect_sv

    @property
    def reconnect_sv(self):
        return self.connector.reconnect_sv

    @property
    def incoming_transaction_data(self):
        return self.connector.incoming_transaction_data

    @property
    def send_transaction_data(self):
        return self.connector.send_transaction_data

    @property
    def transaction_sent(self):
        return self.connector.transaction_sent

    @property
    def stateChanged(self):
        return self.connector.stateChanged

    def __init__(self, config: Config):
        super(ConnectionThread, self).__init__()
        self.config: Config = config
        self.connector: Connector = Connector(self.config)
        self.thread: QThread = QThread()
        self.connector.moveToThread(self.thread)
        self.thread.started.connect(self.run)
        self.thread.start()

    def run(self):
        while not self.stop:
            QCoreApplication.processEvents()
            QThread.msleep(10)

        self.thread.exit()

    def stop_thread(self):
        self.stop = True
