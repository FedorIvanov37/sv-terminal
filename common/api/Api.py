# from waitress import serve
import datetime
from os import getcwd
from os.path import normpath
from flask import Flask, request, redirect, url_for
from flask_pydantic import validate
from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QCoreApplication
from PyQt6.QtNetwork import QTcpSocket
from common.lib.decorators.singleton import singleton
from common.lib.data_models.Transaction import Transaction
from common.api.data_models.types import ApiResponse
from common.lib.data_models.Config import Config
from common.lib.core.Parser import Parser
from pydantic import ValidationError
from http import HTTPStatus, HTTPMethod
from common.lib.data_models.EpaySpecificationModel import EpaySpecModel
from common.api.data_models.Connection import Connection
from common.gui.enums.GuiFilesPath import GuiFilesPath
from common.gui.enums.ConnectionStatus import ConnectionStatus
from common.api.enums.ConnectionActions import ConnectionActions
from common.api.enums.TransTypes import TransTypes
from common.api.data_models.ApiError import ApiError
from common.lib.enums.TermFilesPath import TermFilesPath
from common.api.exceptions.api_exceptions import (
    TransactionTimeout,
    LostTransactionResponse,
    TransactionSendingError,
    HostConnectionTimeout,
    HostConnectionError,
    HostAlreadyConnected,
    HostAlreadyDisconnected,
)


@singleton
class ApiInterface(QObject):
    _create_transaction: pyqtSignal = pyqtSignal(Transaction)
    _terminal = None
    _transaction_timer: QTimer = None
    _config: Config = None
    _spec: EpaySpecModel = None

    @property
    def specification(self):
        return self._spec

    @specification.setter
    def specification(self, specification):
        self._spec = specification

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = Config.model_validate(config)

    @property
    def terminal(self):
        return self._terminal

    @terminal.setter
    def terminal(self, terminal):
        self._terminal = terminal

    @property
    def transaction_timer(self):
        return self._transaction_timer

    @property
    def create_transaction(self):
        return self._create_transaction

    def __init__(self, config: Config | None = None, terminal=None):
        super().__init__()

        if terminal is not None:
            self._terminal = terminal

        if config is not None:
            self.config = config

    def build_connection(self) -> Connection:
        connection = Connection()

        try:
            connection.status = ConnectionStatus[self.terminal.connector.state().name]
        except KeyError:
            connection.status = None

        connection.host = self.terminal.connector.peerAddress().toString()
        connection.port = self.terminal.connector.peerPort()

        return connection

    def connect(self, connection_params: Connection):
        self.terminal.connector.connect_sv(host=connection_params.host, port=connection_params.port)

    def disconnect(self):
        self.terminal.connector.disconnect_sv()

    def build_transactions(self, hide_secrets=False) -> dict[str, dict | str]:
        transactions: dict[str, dict | str] = dict()

        for transaction in self.terminal.trans_queue.queue:
            if hide_secrets:
                transaction: Transaction = Parser.hide_secret_fields(transaction)

            transactions[transaction.trans_id] = transaction.dict()

        return transactions

    def build_reversal(self, transaction_id):
        if not (original_transaction := self.terminal.trans_queue.get_transaction(transaction_id)):
            raise LookupError

        if not original_transaction.matched:
            raise LostTransactionResponse(f"Cannot reverse transaction {transaction_id}. Lost response")

        if not original_transaction.is_request:
            if not (original_transaction := self.terminal.trans_queue.get_transaction(original_transaction.match_id)):
                raise LostTransactionResponse(f"Cannot reverse transaction {transaction_id}. Lost response")

        reversal: Transaction = self.terminal.build_reversal(original_transaction)

        return reversal

    def get_reversible_transactions(self) -> list[Transaction]:
        return self.terminal.trans_queue.get_reversible_transactions()

    def send_transaction(self, transaction: Transaction) -> Transaction | str:
        timeout = 10

        self.create_transaction.emit(transaction)

        if not self.config.api.wait_remote_host_response:
            if self.config.api.hide_secrets:
                transaction: Transaction = Parser.hide_secret_fields(transaction)

            return transaction

        begin = datetime.datetime.now()

        while (datetime.datetime.now() - begin).seconds < timeout and not transaction.matched and not transaction.error:
            QCoreApplication.processEvents()

        if transaction.error:
            raise TransactionSendingError(f"Cannot send transaction: {transaction.error}")

        if not transaction.matched:
            raise TransactionTimeout(f"No remote host transaction response in {timeout} seconds")

        if not (response := self.terminal.trans_queue.get_transaction(transaction.match_id)):
            raise LostTransactionResponse("Lost transaction response")

        if self.config.api.hide_secrets:
            response: Transaction = Parser.hide_secret_fields(response)

        return response

    def update_config(self, config: Config) -> None:
        with open(TermFilesPath.CONFIG, 'w') as config_file:
            config_file.write(config.json())

        self.terminal.config = config
        self.config = config

    @staticmethod
    def get_transaction(trans_type: TransTypes) -> Transaction:
        transaction_files_map = {
            TransTypes.ECHO_TEST: TermFilesPath.ECHO_TEST,
            TransTypes.KEEP_ALIVE: TermFilesPath.KEEP_ALIVE,
            TransTypes.EPOS_PURCHASE: TermFilesPath.DEFAULT_FILE,
        }

        if not (transaction_file := transaction_files_map.get(trans_type)):
            raise TypeError(f"Unknown transaction type '{trans_type}'")

        with open(transaction_file) as transaction_file_data:
            transaction: Transaction = Transaction.model_validate_json(transaction_file_data.read())

        if trans_type == TransTypes.KEEP_ALIVE:
            transaction.is_keep_alive = True

        return transaction

    def update_connection(self, action: ConnectionActions):
        match action:
            case ConnectionActions.RECONNECT:
                target_state: QTcpSocket.SocketState = QTcpSocket.SocketState.ConnectedState

                if self.terminal.connector.state() == target_state:
                    self.update_connection(ConnectionActions.DISCONNECT)

                return self.update_connection(ConnectionActions.CONNECT)

            case ConnectionActions.DISCONNECT:
                target_state: QTcpSocket.SocketState = QTcpSocket.SocketState.UnconnectedState
                connection: Connection = self.build_connection()

                if self.terminal.connector.state() == target_state:
                    raise HostAlreadyDisconnected("The host is already disconnected")

                self.disconnect()

            case ConnectionActions.CONNECT:
                if self.terminal.connector.state() == QTcpSocket.SocketState.ConnectedState:
                    raise HostAlreadyConnected(
                        f"The host is already connected. "
                        f"Disconnect before open new connection or use {ConnectionActions.RECONNECT}"
                    )

                target_state: QTcpSocket.SocketState = QTcpSocket.SocketState.ConnectedState
                connection: Connection = Connection(host=self.config.host.host, port=self.config.host.port)

                if request.content_type == "application/json":
                    connection: Connection = Connection.model_validate(request.get_json())

                self.connect(connection)

            case _:
                raise HostConnectionError(f"Unknown connection action: {action}")

        if self.terminal.connector.state() == target_state:
            connection.status = ConnectionStatus[self.terminal.connector.state().name]
            return connection

        if self.terminal.connector.error() == QTcpSocket.SocketError.SocketTimeoutError:
            raise HostConnectionTimeout(self.terminal.connector.errorString())

        raise HostConnectionError(self.terminal.connector.errorString())


class Api(QObject):
    app: Flask = Flask("SignalApi")
    signal: ApiInterface = ApiInterface()

    def __init__(self, config: Config):
        super(Api, self).__init__()
        self.config = config

    def stop(self):
        raise KeyboardInterrupt

    @staticmethod
    @app.route("/")
    @app.route("/doc")
    @app.route("/docs")
    @app.route("/help")
    @app.route("/api")
    @app.route("/api/")
    @app.route("/api/doc")
    @app.route("/api/docs")
    @app.route("/api/help")
    def redirect_to_document():
        return redirect(url_for("get_document"))

    @staticmethod
    @app.route("/api/documentation")
    def get_document():
        doc_path = normpath(f"{getcwd()}/{GuiFilesPath.DOC}")

        with open(doc_path, encoding="utf8") as html_file:
            return html_file.read()

    @staticmethod
    @app.route("/api/tools/transactions/validate", methods=[HTTPMethod.POST])
    @validate()
    def validate_transaction(body: Transaction):
        transaction: Transaction = body

        if Api.signal.config.api.hide_secrets:
            transaction: Transaction = Parser.hide_secret_fields(transaction)

        return transaction

    @staticmethod
    def send_transaction(transaction: Transaction) -> ApiResponse:
        try:
            response = Api.signal.send_transaction(transaction)

        except TransactionTimeout as transaction_timeout:
            return ApiError(error=transaction_timeout), HTTPStatus.REQUEST_TIMEOUT

        except (LostTransactionResponse, TransactionSendingError) as sending_error:
            return ApiError(error=sending_error), HTTPStatus.UNPROCESSABLE_ENTITY

        except Exception as unhandled_exception:
            return ApiError(error=unhandled_exception), HTTPStatus.INTERNAL_SERVER_ERROR

        return response, HTTPStatus.OK

    @staticmethod
    @app.route("/api/transactions/<string:trans_type>", methods=[HTTPMethod.POST])
    @validate()
    def create_predefined_transaction(trans_type: TransTypes):
        try:
            transaction_request: Transaction = Api.signal.get_transaction(trans_type)

        except Exception as transaction_error:
            return ApiError(error=transaction_error), HTTPStatus.INTERNAL_SERVER_ERROR

        response, status = Api.send_transaction(transaction_request)

        if Api.signal.config.api.hide_secrets and isinstance(response, Transaction):
            response: Transaction = Parser.hide_secret_fields(response)

        return response, status

    @staticmethod
    @app.route("/api/connection/<string:action>", methods=[HTTPMethod.PUT])
    @validate()
    def update_connection(action: ConnectionActions):
        try:
            connection: Connection = Api.signal.update_connection(action)

        except HostAlreadyConnected as host_already_connected:
            connection_error = ApiError(error=str(host_already_connected)).dict()
            connection_error["connection"] = Api.signal.build_connection().dict()

            return connection_error, HTTPStatus.BAD_REQUEST

        except HostAlreadyDisconnected as host_already_connected:
            return ApiError(error=f"Disconnection error: {host_already_connected}"), HTTPStatus.BAD_REQUEST

        except HostConnectionTimeout as host_connection_timeout:
            return ApiError(error=f"Connection error: {host_connection_timeout}"), HTTPStatus.REQUEST_TIMEOUT

        except HostConnectionError as host_connection_error:
            return ApiError(error=f"Connection error: {host_connection_error}"), HTTPStatus.BAD_GATEWAY

        return connection

    @staticmethod
    @app.route("/api/connection", methods=[HTTPMethod.GET])
    @validate()
    def get_connection():
        return Api.signal.build_connection()

    @staticmethod
    @app.route("/api/specification", methods=[HTTPMethod.GET])
    @validate()
    def get_specification():
        signal: ApiInterface = ApiInterface()

        if not signal.specification:
            return ApiError(error="Specification not found"), HTTPStatus.NOT_FOUND

        return signal.specification.spec

    @staticmethod
    @app.route("/api/specification/update", methods=[HTTPMethod.PUT])
    @validate()
    def update_specification(body: EpaySpecModel):
        Api.signal.specification.reload_spec(body, commit=False)
        return Api.signal.specification.spec

    @staticmethod
    @app.route("/api/config/update", methods=[HTTPMethod.PUT])
    @validate()
    def update_config(body: Config):
        Api.signal.update_config(body)
        return Api.signal.config

    @staticmethod
    @app.route("/api/config", methods=[HTTPMethod.GET])
    @validate()
    def get_config():
        if not Api.signal.config:
            return ApiError(error="config not found"), HTTPStatus.NOT_FOUND

        return Api.signal.config

    @staticmethod
    @app.route("/api/transactions/<string:trans_id>", methods=[HTTPMethod.GET])
    @validate()
    def get_transaction(trans_id: str) -> ApiResponse | Transaction:
        transactions = Api.signal.build_transactions(hide_secrets=Api.signal.config.api.hide_secrets)

        if not (transaction := transactions.get(trans_id)):
            return ApiError(error=f"No transaction id '{trans_id}' in transactions queue"), HTTPStatus.NOT_FOUND

        return transaction

    @staticmethod
    @app.route("/api/transactions", methods=[HTTPMethod.GET])
    def get_transactions():
        return Api.signal.build_transactions(hide_secrets=Api.signal.config.api.hide_secrets)

    @staticmethod
    @app.route("/api/transactions/<string:trans_id>/reverse", methods=[HTTPMethod.POST])
    @validate()
    def reverse_transaction(trans_id: str):
        transaction: dict

        if not (transaction := Api.get_transactions().get(trans_id)):
            return ApiError(error=f"No transaction id '{trans_id}' in transactions queue"), HTTPStatus.NOT_FOUND

        transaction: Transaction = Transaction.model_validate(transaction)

        if not transaction.is_request:
            if not (transaction := Api.signal.terminal.trans_queue.get_transaction(transaction.match_id)):
                return ApiError(error="Lost original response"), HTTPStatus.NOT_FOUND

        if transaction.trans_id not in (trans.trans_id for trans in Api.signal.get_reversible_transactions()):
            return (ApiError(error="Cannot reverse transaction. Lost response or non-reversible MTI"),
                    HTTPStatus.UNPROCESSABLE_ENTITY)

        try:
            reversal: Transaction = Api.signal.build_reversal(transaction.trans_id)

        except LookupError:
            return ApiError(error=f"No transaction id '{trans_id}' in transactions queue"), HTTPStatus.NOT_FOUND

        except (ValidationError, ValueError, TypeError) as validation_error:
            return ApiError(error=validation_error), HTTPStatus.UNPROCESSABLE_ENTITY

        except Exception as unhandled_exception:
            return ApiError(error=unhandled_exception), HTTPStatus.INTERNAL_SERVER_ERROR

        return Api.send_transaction(reversal)

    @staticmethod
    @app.route("/api/transactions", methods=[HTTPMethod.POST])
    @validate()
    def create_transaction(body: Transaction):
        return Api.send_transaction(body)

    def run_api(self):
        self.app.json.sort_keys = False
        # waitress_logger = getLogger("waitress")
        # waitress_logger.setLevel(INFO)
        self.app.run(host=self.config.api.address, port=self.config.api.port)
        # serve(self.app, host=self.config.api.address, port=self.config.api.port)
