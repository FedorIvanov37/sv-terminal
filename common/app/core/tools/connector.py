from struct import pack
from PyQt5.QtNetwork import QTcpSocket, QNetworkProxy
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from common.app.core.tools.parser import Parser
from logging import info, error, debug, warning
from common.app.data_models.config import Config
from common.app.data_models.message import Message
from PyQt5.QtWidgets import QApplication
from typing import Optional


class Connector(QTcpSocket):
    def __init__(self, config: Config):
        QTcpSocket.__init__(self)
        self.config = config
        self.parser = Parser(self.config)

    def read_from_socket(self):
        debug("Socket has %d bytes of an incoming data", self.bytesAvailable())
        incoming_data = self.readAll()
        return incoming_data[2:]  # Cut the header

    def connect_sv(self):
        host = self.config.smartvista.host
        port = self.config.smartvista.port

        if "" in (host, port):
            error("Lost SV host address or port number. Check the configuration.")
            return

        port = int(port)

        debug("Connecting to %s:%s", host, port)

        # if not self.config.smartvista.use_proxy:
        #     self.setProxy(QNetworkProxy(QNetworkProxy.NoProxy))

        self.connectToHost(host, port)
        self.waitForConnected(msecs=10000)

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

    def send_message(self, message: Message = None) -> bool:
        if message is None:
            return False

        if self.state() != self.ConnectedState:
            error("Connection with SmartVista is not established")
            return False

        dump: bytes = self.parser.create_dump(message)
        dump = pack("!H", len(dump)) + dump
        bytes_sent = self.write(dump)

        if bytes_sent > int():
            info("Message was sent")
            info("")
            debug("bytes sent %s", bytes_sent)
            self.flush()
            return True

        return False


class ConnectionWorker(QObject):
    _stop: bool = False
    _in_progress: bool = False
    _connector: Connector
    _need_reconnect: bool = False
    _connected: pyqtSignal = pyqtSignal()
    _disconnected: pyqtSignal = pyqtSignal()
    _socket_error: pyqtSignal = pyqtSignal(int)
    _ready_read: pyqtSignal = pyqtSignal()
    _connection_started: pyqtSignal = pyqtSignal()
    _connection_finished: pyqtSignal = pyqtSignal()
    _message_sent: pyqtSignal = pyqtSignal(Message)

    @property
    def message_sent(self):
        return self._message_sent

    @property
    def connected(self):
        return self.connector.connected

    @property
    def connection_started(self):
        return self._connection_started

    @property
    def connection_finished(self):
        return self._connection_finished

    @property
    def ready_read(self):
        return self._ready_read

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
    def in_progress(self):
        return self._in_progress

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, stop):
        self._stop = stop

    @property
    def connector(self):
        return self._connector

    @connector.setter
    def connector(self, connector):
        self._connector = connector

    def __init__(self, config):
        super(ConnectionWorker, self).__init__()
        self.connector = Connector(config)
        self.connector.connected.connect(self.connected.emit)
        self.connector.disconnected.connect(self.disconnected.emit)
        self.connector.readyRead.connect(self.ready_read.emit)
        self.connector.disconnected.connect(lambda: self.socker_error.emit(self.connector.error()))
        self.connector.errorOccurred.connect(lambda sock_err: self.socker_error.emit(sock_err))
        self.message: Optional[Message] = None

    def run(self):
        self._in_progress = True

        while not self._stop:
            QApplication.processEvents()
            QThread.msleep(10)

        self._in_progress = False

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

    def read_from_socket(self):
        return self.connector.read_from_socket()

    def send_message(self, message: Message):
        if self.connector.state() != self.connector.ConnectedState:
            warning("Connection is not Established, trying to connect")
            self.connect_sv()

        if self.connector.state() != self.connector.ConnectedState:
            error("Cannot establish the connection with SmartVista")
            return

        if self.connector.send_message(message):
            self.message_sent.emit(message)
            return

        error("The message wasn't sent")

    def disconnect_sv(self):
        self.connector.abort()
