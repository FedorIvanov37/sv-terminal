from struct import pack
from json import loads
from requests import get
from logging import error, debug, warning, info
from PyQt6.QtNetwork import QTcpSocket
from PyQt6.QtCore import pyqtSignal, Qt
from common.lib.data_models.Config import Config
from common.lib.interfaces.MetaClasses import QObjectAbcMeta
from common.lib.interfaces.ConnectorInterface import ConnectionInterface
from common.lib.data_models.EpaySpecificationModel import EpaySpecModel
from common.lib.core.EpaySpecification import EpaySpecification


class Connector(QTcpSocket, ConnectionInterface, metaclass=QObjectAbcMeta):
    incoming_transaction_data: pyqtSignal = pyqtSignal(bytes)
    transaction_sent: pyqtSignal = pyqtSignal(str)
    startup_finished: bool = False

    def __init__(self, config: Config):
        QTcpSocket.__init__(self)
        self.config = config
        self.readyRead.connect(self.read_transaction_data)

    def connection_in_progress(self):
        return self.state() == self.SocketState.ConnectingState

    def send_transaction_data(self, trans_id: str, transaction_data: bytes):
        if not self.state() == self.SocketState.ConnectedState:
            warning("Host disconnected. Trying to established the connection")

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

    def set_remote_spec(self, app_state):
        if app_state != Qt.ApplicationState.ApplicationActive:
            return

        if self.startup_finished:
            return

        if not self.config.remote_spec.use_remote_spec:
            return

        info(f"Getting remote spec using url: {self.config.remote_spec.remote_spec_url}")

        try:
            resp = get(self.config.remote_spec.remote_spec_url)
        except Exception as spec_loading_error:
            error(f"Cannot get remote spec: {spec_loading_error}")
            self.startup_finished = True
            return

        if not resp.ok:
            error(f"Cannot get remote spec: Non-success http-code {resp.status_code}")
            self.startup_finished = True
            return

        spec: EpaySpecification = EpaySpecification()

        if self.config.remote_spec.rewrite_local_spec:
            backup_filename: str = spec.backup()
            info(f"Local spec will be rewritten. Backup filename: {backup_filename}")

        try:
            spec_data: EpaySpecModel = EpaySpecModel.model_validate(loads(resp.text))
            spec.reload_spec(spec=spec_data, commit=self.config.remote_spec.rewrite_local_spec)
            info(f"Remote specification loaded {spec.spec.name}")

        except Exception as loading_error:
            error(f"Cannot load remote Specification: {loading_error}")
            info("Use local specification instead")

        finally:
            self.startup_finished = True
