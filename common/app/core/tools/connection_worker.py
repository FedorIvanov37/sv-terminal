from logging import error, warning
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from common.lib.data_models.Transaction import Transaction
from common.lib.Connector import Connector


class ConnectionWorker(QObject):
    _connector: Connector
    _need_reconnect: bool = False
    _connected: pyqtSignal = pyqtSignal()
    _disconnected: pyqtSignal = pyqtSignal()
    _socket_error: pyqtSignal = pyqtSignal(int)
    _connection_started: pyqtSignal = pyqtSignal()
    _connection_finished: pyqtSignal = pyqtSignal()
    _transaction_sent: pyqtSignal = pyqtSignal(Transaction)
    _transaction_received: pyqtSignal = pyqtSignal(Transaction)
    _stop: bool = False

    @property
    def transaction_received(self):
        return self._transaction_received

    @property
    def error_string(self):
        return self.connector.errorString()

    @property
    def transaction_sent(self):
        return self._transaction_sent

    @property
    def connection_started(self):
        return self._connection_started

    @property
    def connection_finished(self):
        return self._connection_finished

    @property
    def socker_error(self):
        return self._socket_error

    @property
    def connected(self):
        return self._connected

    @property
    def disconnected(self):
        return self._disconnected

    @property
    def connector(self):
        return self._connector

    @connector.setter
    def connector(self, connector):
        self._connector = connector

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, stop):
        self._stop = stop

    def __init__(self, config):
        super(ConnectionWorker, self).__init__()
        self.connector = Connector(config)
        self.connector.connected.connect(self.connected.emit)
        self.connector.disconnected.connect(self.disconnected.emit)
        self.connector.readyRead.connect(self.connector.read_transaction_data)
        self.connector.incoming_message.connect(self.transaction_received)
        self.connector.disconnected.connect(lambda: self.socker_error.emit(self.connector.error()))
        self.connector.errorOccurred.connect(lambda sock_err: self.socker_error.emit(sock_err))

    def run(self):
        while not self.stop:
            QApplication.processEvents()
            QThread.msleep(10)

    def error(self):
        return self.connector.error()

    def connect_sv(self):
        try:
            self._connection_started.emit()
            self.connector.reconnect_sv()
        except Exception as e:
            error(e)
        else:
            self.connection_finished.emit()

    def send_transaction(self, transaction: Transaction):
        if self.connector.state() != self.connector.SocketState.ConnectedState:
            warning("Connection is not Established, trying to connect")
            self.connect_sv()

        if self.connector.state() != self.connector.SocketState.ConnectedState:
            error(f"Cannot establish the connection to SmartVista: {self.connector.errorString()}")
            return

        if self.connector.send_transaction(transaction):
            self._transaction_sent.emit(transaction)
            return

        error("The transaction wasn't sent")

    def disconnect_sv(self):
        self.connector.abort()
