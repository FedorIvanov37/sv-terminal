from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from http import HTTPStatus
from uvicorn import run as run_api
from PyQt6.QtCore import QObject, pyqtSignal
from common.lib.data_models.Transaction import Transaction
from common.lib.decorators.singleton import singleton
from common.lib.core.TransactionQueue import TransactionQueue
from common.lib.data_models.Config import Config
from common.lib.core.Connector import Connector
from common.api.data_models.Connection import Connection
from common.gui.enums.ConnectionStatus import ConnectionStatus
from common.api.enums.ConnectionActions import ConnectionActions


@singleton
class SignalApiConnector(QObject):
    _incoming_transaction: pyqtSignal = pyqtSignal(Transaction)
    _trans_queue: TransactionQueue
    _config: Config
    _tcp_connector: Connector

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

    def get_transaction(self, trans_id):
        return self.trans_queue.get_transaction(trans_id)


class SignalApi(QObject):
    app: FastAPI = FastAPI()
    connector: SignalApiConnector = SignalApiConnector()

    def __init__(self):
        super().__init__()

    @staticmethod
    @app.get("/", response_class=RedirectResponse)
    def root():
        return RedirectResponse("/api/documentation")

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
    @app.get("/api/documentation", response_class=HTMLResponse)
    def render_document():
        with open("Signal_v0.18.html", "r", encoding="utf-8") as html_data:
            return HTMLResponse(content=html_data.read(), status_code=HTTPStatus.OK)

    @staticmethod
    @app.post("/api/transactions/create", response_model=Transaction)
    def create_transaction(transaction: Transaction):
        SignalApi.connector.incoming_transaction.emit(transaction)

        begin = datetime.now()

        while not transaction.matched:
            if transaction.matched:
                return SignalApi.connector.get_transaction(transaction.match_id)

            if (datetime.now() - begin).seconds > 60 and not transaction.matched:
                raise HTTPException(status_code=HTTPStatus.GATEWAY_TIMEOUT, detail="Transaction response timeout")

        return transaction

    def run(self):
        run_api(self.app, host="0.0.0.0")

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
