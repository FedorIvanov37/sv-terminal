from json import dumps
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.requests import Request
from http import HTTPStatus
from uvicorn import run as run_api
from PyQt6.QtCore import QObject, pyqtSignal, QCoreApplication
from common.lib.data_models.Transaction import Transaction
from common.lib.decorators.singleton import singleton
from common.lib.core.TransactionQueue import TransactionQueue
from common.lib.data_models.Config import Config
from common.lib.core.Connector import Connector
from common.api.data_models.Connection import Connection
from common.gui.enums.ConnectionStatus import ConnectionStatus
from common.api.enums.ConnectionActions import ConnectionActions
from common.lib.data_models.EpaySpecificationModel import EpaySpecModel
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.exceptions.exceptions import DataValidationError, DataValidationWarning
from common.lib.enums.DataFormats import OutputFilesFormat
from common.lib.core.LogStream import LogStream
import logging


@singleton
class SignalApiConnector(QObject):
    _incoming_transaction: pyqtSignal = pyqtSignal(Transaction)
    _reverse_transaction: pyqtSignal = pyqtSignal(str)
    _trans_queue: TransactionQueue
    _config: Config
    _tcp_connector: Connector
    _terminal = None
    _log_handler = None

    @property
    def log_handler(self):
        return self._log_handler

    @log_handler.setter
    def log_handler(self, log_handler):
        self._log_handler = log_handler

    @property
    def terminal(self):
        return self._terminal

    @terminal.setter
    def terminal(self, terminal):
        self._terminal = terminal

    @property
    def reverse_transaction(self):
        return self._reverse_transaction

    @property
    def tcp_connector(self):
        return self._tcp_connector

    @tcp_connector.setter
    def tcp_connector(self, tcp_connector):
        self._tcp_connector = tcp_connector

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    @property
    def trans_queue(self):
        return self._trans_queue

    @trans_queue.setter
    def trans_queue(self, trans_queue):
        self._trans_queue = trans_queue

    @property
    def incoming_transaction(self):
        return self._incoming_transaction

    def __init__(self):
        super().__init__()

    def validate_transaction(self, transaction: Transaction):
        self.terminal.validate(transaction)

    def get_transaction(self, trans_id):
        return self.trans_queue.get_transaction(trans_id)


class SignalApi(QObject):
    app: FastAPI = FastAPI(title="Signal API", debug=False)
    connector: SignalApiConnector = SignalApiConnector()

    def __init__(self, stream):
        super().__init__()
        self.stream = stream

    @staticmethod
    @app.get("/api/transactions", response_model=list[Transaction])
    def get_transactions():
        return list(SignalApi.connector.trans_queue.queue)

    @staticmethod
    @app.get("/api/transactions/{trans_id}", response_model=Transaction)
    def get_transactions(trans_id: str):
        if not (transaction := SignalApi.connector.trans_queue.get_transaction(trans_id)):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Transaction ID {trans_id} does not found")

        return transaction

    @staticmethod
    @app.put("/api/connection/{action}", response_model=Connection)
    def update_connection(action: ConnectionActions, connection: Connection | None = None):
        if action == ConnectionActions.DISCONNECT:
            SignalApi.connector.tcp_connector.disconnect_sv()

        if action == ConnectionActions.CONNECT:
            if connection is None:
                SignalApi.connector.tcp_connector.connect_sv()
                return SignalApi.build_connection()

            if not connection.host:
                SignalApi.connector.config.host.host = connection.host

            if not connection.port:
                SignalApi.connector.config.host.port = connection.port

            SignalApi.connector.tcp_connector.connect_sv()

        return SignalApi.build_connection()

    @staticmethod
    @app.get("/api/connection", response_model=Connection)
    def get_connection():
        return SignalApi.build_connection()

    @staticmethod
    @app.get("/api/config", response_model=Config)
    def get_config():
        return SignalApi.connector.config

    @staticmethod
    @app.put("/api/config/update", response_model=Config)
    def put_config(config: Config):
        SignalApi.connector.config.__dict__ = config.__dict__
        return SignalApi.connector.config

    @staticmethod
    @app.get("/")
    @app.get("/doc")
    @app.get("/docs")
    @app.get("/help")
    @app.get("/documentation")
    @app.get("/api")
    @app.get("/api/doc")
    @app.get("/api/docs")
    @app.get("/api/help")
    @app.get("/api/documentation", response_class=HTMLResponse)
    def render_document():
        with open("Signal_v0.18.html", "r", encoding="utf-8") as html_data:
            return HTMLResponse(content=html_data.read(), status_code=HTTPStatus.OK)

    @staticmethod
    @app.get("/api/specification", response_model=EpaySpecModel)
    def get_specification():
        return EpaySpecification().spec

    @staticmethod
    @app.post("/api/tools/transactions/validate")
    def validate_transaction(transaction: Transaction):
        try:
            SignalApi.connector.terminal.trans_validator.validate_transaction(transaction)

        except DataValidationWarning as data_validation_warning:
            data_validation_warning: str = str(data_validation_warning).replace("\n", "; ")
            return {"Validation warnings": data_validation_warning}

        except DataValidationError as data_validation_error:
            data_validation_error: str = str(data_validation_error).replace("\n", "; ")
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=data_validation_error)

        return {"Validation result": "Transaction data validated"}

    @staticmethod
    @app.post("/api/tools/transactions/convert", response_class=Response)
    def convert_transaction(transaction: Transaction, to_format: OutputFilesFormat):
        match to_format:
            case OutputFilesFormat.INI:
                return SignalApi.connector.terminal.parser.transaction_to_ini_string(transaction)

            case OutputFilesFormat.JSON:
                return dumps(transaction.dict(), indent=4)

            case OutputFilesFormat.DUMP:
                return SignalApi.connector.terminal.parser.create_sv_dump(transaction)

            case _:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    @staticmethod
    @app.post("/api/tools/parse/{data_format}", response_model=Transaction)
    async def parse_transaction_data(request: Request, data_format: OutputFilesFormat):
        data = await request.body()
        data = data.decode()

        match data_format:
            case OutputFilesFormat.JSON:
                return Transaction.parse_raw(data)

            case OutputFilesFormat.DUMP:
                raise HTTPException(status_code=HTTPStatus.NOT_IMPLEMENTED, detail="Dump not supported")
                # return SignalApi.connector.terminal.parser.parse_dump(data)

            case OutputFilesFormat.INI:
                return SignalApi.connector.terminal.parser.parse_ini_string(data)

    @staticmethod
    @app.put("/api/specification/update", response_model=EpaySpecModel)
    def update_specification(specification: EpaySpecModel):
        spec: EpaySpecification = EpaySpecification()
        spec.spec.fields = specification.fields

        return spec.spec

    @staticmethod
    @app.get("/api/status")
    def api_status():
        return {
            "API status": "UP",
            "GUI status": "RUN",
            "Connection": SignalApi.get_connection()
        }

    @staticmethod
    @app.post("/api/transactions/create", response_model=Transaction)
    def create_transaction(transaction: Transaction):
        SignalApi.connector.incoming_transaction.emit(transaction)

        begin = datetime.now()

        while not transaction.matched:
            QCoreApplication.processEvents()

            if transaction.matched:
                return SignalApi.connector.get_transaction(transaction.match_id)

            if (datetime.now() - begin).seconds > 60 and not transaction.matched:
                raise HTTPException(status_code=HTTPStatus.GATEWAY_TIMEOUT, detail="Transaction response timeout")

        return SignalApi.connector.get_transaction(transaction.match_id)

    @staticmethod
    @app.post("/api/transactions/{trans_id}/reverse", response_model=Transaction)
    def reverse_transaction(trans_id: str):
        if not (original := SignalApi.connector.get_transaction(trans_id)):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Original transaction {trans_id} is not found")

        if not (original := SignalApi.connector.get_transaction(original.match_id)):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Original transaction {trans_id} is not found")

        if not (reversal := SignalApi.connector.terminal.build_reversal(original)):
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Cannot generate reversal")

        SignalApi.connector.incoming_transaction.emit(reversal)

        begin = datetime.now()

        while not reversal.matched:
            QCoreApplication.processEvents()

            if reversal.matched:
                return SignalApi.connector.get_transaction(reversal.match_id)

            if (datetime.now() - begin).seconds > 60 and not reversal.matched:
                raise HTTPException(status_code=HTTPStatus.GATEWAY_TIMEOUT, detail="Transaction response timeout")

        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Unhandled error")

    def run(self):
        log_config_dict = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(levelprefix)s %(message)s",
                    "use_colors": None,
                },
                "access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
                "access": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "uvicorn": {"handlers": [], "level": "INFO", "propagate": False},
                "uvicorn.error": {"level": "CRITICAL"},
                "uvicorn.access": {"handlers": [], "level": "INFO", "propagate": False},
            },
        }

        run_api(self.app, host=SignalApi.connector.config.api.address, port=SignalApi.connector.config.api.port, log_config=log_config_dict) #

    def stop_api(self):
        raise KeyboardInterrupt

    @staticmethod
    def build_connection() -> Connection:
        connection = Connection()

        try:
            connection.status = ConnectionStatus[SignalApi.connector.tcp_connector.state().name]
        except KeyError:
            connection.status = None

        connection.host = SignalApi.connector.tcp_connector.peerAddress().toString()
        connection.port = SignalApi.connector.tcp_connector.peerPort()

        return connection
