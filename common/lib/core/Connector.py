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
from common.lib.data_models.EpaySpecificationModel import EpaySpecModel
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.enums.TermFilesPath import TermDirs
from common.lib.core.SpecFilesRotator import SpecFilesRotator
from common.lib.core.validators.DataValidator import DataValidator
from common.lib.exceptions.exceptions import DataValidationError, DataValidationWarning


class Connector(QTcpSocket, ConnectionInterface, metaclass=QObjectAbcMeta):
    incoming_transaction_data: pyqtSignal = pyqtSignal(bytes)
    transaction_sent: pyqtSignal = pyqtSignal(str)
    got_remote_spec: pyqtSignal = pyqtSignal()

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

    def set_remote_spec(self, commit=None):
        if commit is None:
            commit = self.config.specification.rewrite_local_spec

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
            try:
                resp: HTTPResponse | str = urlopen(self.config.specification.remote_spec_url)
            except Exception as spec_loading_error:
                error(f"Cannot get remote specification: {spec_loading_error}")
                warning(use_local_spec_text)
                return

            if resp.getcode() != HTTPStatus.OK:
                error(f"Cannot get remote specification: Non-success http-code {resp.status}")
                warning(use_local_spec_text)
                return

            spec: EpaySpecification = EpaySpecification()

            if commit and self.config.specification.backup_storage:
                rotator: SpecFilesRotator = SpecFilesRotator()
                backup_filename: str = rotator.backup_spec()
                debug(f"Backup local specification file name: {TermDirs.SPEC_BACKUP_DIR}/{backup_filename}")

            try:
                spec_data: EpaySpecModel = EpaySpecModel.model_validate_json(resp.read())
                spec.reload_spec(spec=spec_data, commit=commit)

                info(f"Remote specification loaded: {spec.spec.name}")

                self.got_remote_spec.emit()

            except Exception as loading_error:
                error(f"Cannot load remote specification: {loading_error}")
                warning(use_local_spec_text)

        except Exception as spec_error:
            error(f"Cannot load remote specification: {spec_error}")
