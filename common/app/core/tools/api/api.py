from threading import Thread
from PyQt5.QtCore import QObject
from common.app.data_models.config import Config
# from common.app.core.tools.api.app import run_api
from common.app.core.tools.api.adapter import QtAdapter



class TerminalApi(QObject):
    _state: bool = False
    _adapter: QtAdapter = QtAdapter()
    _thread: Thread = None

    @property
    def adapter(self):
        return self._adapter

    @adapter.setter
    def adapter(self, adapter):
        self._adapter = adapter

    @property
    def state(self):
        return self._state

    def __init__(self, config: Config) -> None:
        super(TerminalApi, self).__init__()
        self.config = config
        self.adapter = QtAdapter()

    @state.setter
    def state(self, state):
        self._state = state

    def run(self):
        # self._thread = run_api(host="127.0.0.1", port=self.config.smartvista.api_port)
        self.state = True
