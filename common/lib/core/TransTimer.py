from logging import info
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from common.lib.constants import KeepAliveIntervals


class TransactionTimer(QObject):
    _trans_loop_timer: QTimer = QTimer()
    _send_transaction: pyqtSignal = pyqtSignal()
    _interval_was_set: pyqtSignal = pyqtSignal(str)

    @property
    def send_transaction(self):
        return self._send_transaction

    @property
    def interval_was_set(self):
        return self._interval_was_set

    def __init__(self, trans_type: str = KeepAliveIntervals.TRANS_TYPE_TRANSACTION):
        super().__init__()
        self.trans_type = trans_type

    def activate_transaction_loop(self, interval: int):
        self._trans_loop_timer.stop()
        self._trans_loop_timer = QTimer()
        self._trans_loop_timer.timeout.connect(self.send_transaction)
        self._trans_loop_timer.start(int(interval) * 1000)

    def set_trans_loop_interval(self, interval_name: str):
        if interval_name == KeepAliveIntervals.KEEP_ALIVE_ONCE:
            self.send_transaction.emit()
            return

        if interval_name == KeepAliveIntervals.KEEP_ALIVE_STOP:
            self._trans_loop_timer.stop()
            info(f"{self.trans_type} loop is deactivated")

        if interval := KeepAliveIntervals.get_interval_time(interval_name):
            self.activate_transaction_loop(interval)
            info(f"{self.trans_type} repeat set to {interval} second(s)")

        self.interval_was_set.emit(interval_name)
