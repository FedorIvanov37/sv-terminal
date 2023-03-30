from struct import pack
from logging import error, debug
from PyQt6.QtNetwork import QTcpSocket
from PyQt6.QtCore import pyqtSignal
from .Parser import Parser
from .data_models.Config import Config
from .data_models.Transaction import Transaction


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

        if not self.state() == self.SocketState.ConnectedState:
            error("Cannot connect SV: SmartVista Host Connection Timeout")

    def disconnect_sv(self):
        if self.state() == QTcpSocket.SocketState.UnconnectedState:
            return

        self.disconnectFromHost()
        self.waitForDisconnected(msecs=10000)

    def reconnect_sv(self):
        for retry in range(3):
            if self.state() == self.SocketState.UnconnectedState:
                break

            self.disconnect_sv()

        else:
            error("Cannot disconnect SmartVista host")
            return

        self.connect_sv()

    def send_transaction(self, transaction: Transaction = None) -> bool:
        if transaction is None:
            return False

        if self.state() != self.SocketState.ConnectedState:
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
