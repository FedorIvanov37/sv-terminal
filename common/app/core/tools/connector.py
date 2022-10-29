from struct import pack
from logging import error, debug, warning
from PyQt5.QtWidgets import QApplication
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from common.app.core.tools.parser import Parser
from common.app.data_models.config import Config
from common.app.data_models.transaction import Transaction


class Connector(QTcpSocket):
    _incoming_message: pyqtSignal = pyqtSignal(Transaction)

    @property
    def incoming_message(self):
        return self._incoming_message

    def __init__(self, config: Config):
        QTcpSocket.__init__(self)
        self.config = config
        self.parser = Parser(self.config)

    def read_from_socket(self):
        debug("Socket has %d bytes of an incoming data", self.bytesAvailable())
        incoming_data = self.readAll()
        return incoming_data[2:]  # Cut the header

    def read_transaction_data(self):
        data = self.read_from_socket().data()

        try:
            transaction: Transaction = self.parser.parse_dump(data=data)
        except Exception as parsing_error:
            error("Incoming transaction parsing error: %s", parsing_error)
            return

        self.incoming_message.emit(transaction)

    def connect_sv(self):
        host = self.config.smartvista.host
        port = self.config.smartvista.port

        if "" in (host, port):
            error("Lost SV host address or port number. Check the configuration.")
            return

        port = int(port)

        debug("Connecting to %s:%s", host, port)

        self.connectToHost(host, port)
        self.waitForConnected(msecs=10000)

        if not self.state() == self.ConnectedState:
            error(f"Cannot open the connection to SVFE: {self.errorString()}")

    def disconnect_sv(self):
        self.disconnectFromHost()
        self.waitForDisconnected(msecs=10000)

    def reconnect_sv(self):
        if self.state() == self.ConnectedState:
            self.disconnect_sv()

        if self.state() != self.UnconnectedState:
            self.abort()
            self.waitForDisconnected(msecs=10000)

        self.connect_sv()

    def send_transaction(self, transaction: Transaction = None) -> bool:
        if transaction is None:
            return False

        if self.state() != self.ConnectedState:
            error("Connection with SmartVista is not established")
            return False

        dump: bytes = self.parser.create_dump(transaction)
        dump = pack("!H", len(dump)) + dump
        bytes_sent = self.write(dump)

        if bytes_sent > int():
            debug("bytes sent %s", bytes_sent)
            self.flush()
            return True

        return False


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

    def error_string(self):
        return self.connector.errorString()

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
        if self.connector.state() != self.connector.ConnectedState:
            warning("Connection is not Established, trying to connect")
            self.connect_sv()

        if self.connector.state() != self.connector.ConnectedState:
            error("Cannot establish the connection to SmartVista")
            return

        if self.connector.send_transaction(transaction):
            self._transaction_sent.emit(transaction)
            return

        error("The transaction wasn't sent")

    def disconnect_sv(self):
        self.connector.abort()
