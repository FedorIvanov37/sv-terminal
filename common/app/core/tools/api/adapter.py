from PyQt5.QtCore import QObject, pyqtSignal
from common.app.decorators.singleton import singleton
from common.app.data_models.message import Message


@singleton
class QtAdapter(QObject):
    _message_ready: pyqtSignal = pyqtSignal(Message)

    @property
    def message_ready(self):
        return self._message_ready

    def emit_message_ready(self, message: Message) -> None:
        self.message_ready.emit(message)
