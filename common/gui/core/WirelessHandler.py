from PyQt6.QtCore import QObject, pyqtSignal
from logging import StreamHandler, LogRecord
from logging import error


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
            self.new_record_appeared.emit(self.format(record))

        except Exception as exc:
            error("Log writing error: %s" % str(exc))
