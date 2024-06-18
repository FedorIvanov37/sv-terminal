from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from http import HTTPStatus
from uvicorn import run as run_api
from PyQt6.QtCore import QObject
from common.lib.data_models.Transaction import Transaction


class SignalApi(QObject):
    app: FastAPI = FastAPI()

    def __init__(self):
        super().__init__()

    @staticmethod
    @app.get("/api/documentation", response_class=HTMLResponse)
    def render_document():
        with open("Signal_v0.18.html", "r", encoding="utf-8") as html_data:
            return HTMLResponse(content=html_data.readlines(), status_code=HTTPStatus.OK)

    @staticmethod
    @app.post("/api/transactions/create", response_model=Transaction)
    def create_transaction(transaction: Transaction):
        return transaction

    def run(self):
        run_api(self.app)
