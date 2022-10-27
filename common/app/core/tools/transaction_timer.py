from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from common.app.data_models.transaction import Transaction


class TransactionTimer(QObject):
    _timeout: int = int
    _timer: QTimer = QTimer()
    _transaction: Transaction = None
    _got_timeout: pyqtSignal = pyqtSignal(Transaction)

    @property
    def got_timeout(self):
        return self._got_timeout

    def __int__(self, transaction: Transaction, timeout=60):
        self._transaction = transaction
        self._timeout = timeout * 1000
        self._timer.timeout.connect(self._got_timeout.emit(self._transaction))

    def start(self):
        self._timer.singleShot(self._timeout)
