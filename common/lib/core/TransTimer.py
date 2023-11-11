from logging import info
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from common.lib.constants import KeepAliveIntervals


class TransactionTimer(QObject):
    trans_loop_timer: QTimer = QTimer()
    send_transaction: pyqtSignal = pyqtSignal()
    interval_was_set: pyqtSignal = pyqtSignal(str)

    def __init__(self, trans_type: str = KeepAliveIntervals.TRANS_TYPE_TRANSACTION):
        super().__init__()
        self.trans_type = trans_type

    def activate_transaction_loop(self, interval: int):
        self.trans_loop_timer.stop()
        self.trans_loop_timer = QTimer()
        self.trans_loop_timer.timeout.connect(self.send_transaction)
        self.trans_loop_timer.start(int(interval) * 1000)

    def set_trans_loop_interval(self, interval_name: str):
        if interval_name == KeepAliveIntervals.KEEP_ALIVE_ONCE:
            self.send_transaction.emit()
            return

        if interval_name == KeepAliveIntervals.KEEP_ALIVE_STOP:
            self.trans_loop_timer.stop()
            info(f"{self.trans_type} loop is deactivated")

        if interval := KeepAliveIntervals.get_interval_time(interval_name):
            self.activate_transaction_loop(interval)
            info(f"{self.trans_type} repeat set to {interval} second(s)")

        self.interval_was_set.emit(interval_name)
