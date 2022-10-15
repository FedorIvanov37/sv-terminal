import uvicorn
from fastapi import FastAPI
from PyQt5.QtCore import QObject, pyqtSignal
from common.app.core.tools.terminal import Terminal
from common.app.data_models.message import Message
from common.app.decorators.singleton import singleton


@singleton
class Adapter(QObject):
    _got_incomint_message: pyqtSignal = pyqtSignal(Message)

    @property
    def got_incominf_message(self):
        return self._got_incomint_message


app = FastAPI()
adapter = Adapter()


class FastApiApp(QObject):
    def __init__(self, terminal: Terminal = None, config=None):
        super(FastApiApp, self).__init__()
        self.setup()

    def setup(self):
        pass

    def run_api(self):
        uvicorn.run(app, host='0.0.0.0', port=8000)

    @app.post("/")
    def create_transaction(message: Message):
        return {"hello": "world"}

    @app.get("/transactions/{trans_id}")
    async def get_transaction(trans_id):
        return {
            "config": {
                "generate_fields": [
                    7,
                    11
                ],
                "max_amount": 0
            },
            "transaction": {
                "message_type_indicator": "0800",
                "id": trans_id,
                "fields": {
                    "7": "0000000000",
                    "11": "000000",
                    "70": "301"
                }
            }
        }


FastApiApp().run_api()


class ApiWorker(QObject):
    _stop: bool = False
    _in_progress: bool = False
    _api: FastApiApp
    _got_incomint_message: pyqtSignal = pyqtSignal(Message)

    @property
    def got_incomint_message(self):
        return self._got_incomint_message

    def __init__(self):
        super(ApiWorker, self).__init__()


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
