from PyQt6.QtCore import QObject, pyqtSignal
from logging import StreamHandler, LogRecord
from common.lib.decorators.singleton import singleton


@singleton
class WirelessHandler(StreamHandler, QObject):
    _new_record_appeared = pyqtSignal(str)
    _last_message: str = str()

    @property
    def new_record_appeared(self):
        return self._new_record_appeared

    def __init__(self):
        StreamHandler.__init__(self)
        QObject.__init__(self)

    def emit(self, record: LogRecord):
        try:
            record = self.format(record)
            self.new_record_appeared.emit(record)

        except Exception:
            return
