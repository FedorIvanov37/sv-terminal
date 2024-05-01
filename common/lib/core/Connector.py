from struct import pack
from http import HTTPStatus
from http.client import HTTPResponse
from urllib.request import urlopen
from logging import error, debug, warning, info
from pydantic import ValidationError
from PyQt6.QtNetwork import QTcpSocket
from PyQt6.QtCore import pyqtSignal
from common.lib.data_models.Config import Config
from common.lib.interfaces.MetaClasses import QObjectAbcMeta
from common.lib.interfaces.ConnectorInterface import ConnectionInterface
from common.lib.core.validators.DataValidator import DataValidator
from common.lib.exceptions.exceptions import DataValidationError, DataValidationWarning


class Connector(QTcpSocket, ConnectionInterface, metaclass=QObjectAbcMeta):
    incoming_transaction_data: pyqtSignal = pyqtSignal(bytes)
    transaction_sent: pyqtSignal = pyqtSignal(str)
    got_remote_spec: pyqtSignal = pyqtSignal(str)

    def __init__(self, config: Config):
        QTcpSocket.__init__(self)
        self.config = config
        self.readyRead.connect(self.read_transaction_data)

    def connection_in_progress(self):
        return self.state() == self.SocketState.ConnectingState

    def send_transaction_data(self, trans_id: str, transaction_data: bytes):
        if not self.state() == self.SocketState.ConnectedState:
            warning("Host disconnected. Trying to establish the connection")

            try:
                self.reconnect_sv()
            except Exception as connection_error:
                error(connection_error)
                return

        if not self.state() == self.SocketState.ConnectedState:
            return

        transaction_header = pack("!H", len(transaction_data))
        transaction_data = transaction_header + transaction_data
        bytes_sent = self.write(transaction_data)

        if bytes_sent == int():
            error("Cannot send transaction data")
            return

        debug("bytes sent %s", bytes_sent)

        self.flush()
        self.transaction_sent.emit(trans_id)

    def read_transaction_data(self):
        debug("Socket has %d bytes of an incoming data", self.bytesAvailable())
        incoming_data = self.readAll()
        incoming_data = incoming_data.data()
        debug(incoming_data)
        self.incoming_transaction_data.emit(incoming_data)

    def connect_sv(self):
        host = self.config.host.host
        port = self.config.host.port

        if "" in (host, port):
            error("Lost SV host address or port number. Check the configuration.")
            return

        port = int(port)

        debug("Connecting to %s:%s", host, port)

        self.connectToHost(host, port)

        self.waitForConnected(msecs=10000)

        if self.state() is self.SocketState.ConnectedState:
            return

        if self.error() is not QTcpSocket.SocketError.SocketTimeoutError:
            return

        self.errorOccurred.emit(QTcpSocket.SocketError.SocketTimeoutError)

    def disconnect_sv(self):
        if not self.state() == QTcpSocket.SocketState.ConnectedState:
            return

        self.disconnectFromHost()

        if not self.state() == QTcpSocket.SocketState.UnconnectedState:
            self.waitForDisconnected(msecs=10000)

    def reconnect_sv(self):
        for retry in range(3):

            if self.state() == self.SocketState.UnconnectedState:
                break

            self.disconnect_sv()

        else:
            error("Cannot disconnect the host")
            return

        try:
            self.connect_sv()

        except Exception as connection_error:
            error(f"SV connection error: {connection_error}")

    def is_connected(self):
        return self.state() == self.SocketState.ConnectedState

    def get_remote_spec(self):
        validator = DataValidator(self.config)

        try:
            validator.validate_url(self.config.specification.remote_spec_url)

        except DataValidationWarning as url_validation_warning:
            warning(url_validation_warning)

        except (ValidationError, DataValidationError) as url_validation_error:
            error(f"Cannot load remote specification due to incorrect URL: {url_validation_error}")
            return

        info(f"Getting remote spec using url {self.config.specification.remote_spec_url}")

        use_local_spec_text = "Local specification will be used instead"

        try:
            resp: HTTPResponse | str = urlopen(self.config.specification.remote_spec_url)

        except Exception as spec_loading_error:
            error(f"Cannot get remote specification: {spec_loading_error}")
            warning(use_local_spec_text)
            return

        try:
            if resp.getcode() != HTTPStatus.OK:
                error(f"Cannot get remote specification: Non-success http-code {resp.status}")
                warning(use_local_spec_text)
                return

            spec_data: str = resp.read().decode()

            self.got_remote_spec.emit(spec_data)

        except Exception as spec_error:
            error(f"Cannot load remote specification: {spec_error}")
            warning(use_local_spec_text)
