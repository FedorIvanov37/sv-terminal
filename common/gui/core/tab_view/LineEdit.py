from PyQt6.QtWidgets import QLineEdit, QWidget
from PyQt6.QtGui import QFont


class LineEdit(QLineEdit):
    def __init__(self, parent: QWidget | None = None):
        super(LineEdit, self).__init__(parent=parent)
        self._setup()

    def _setup(self):
        self.setFont(QFont("Calibri", 12))
        self.setReadOnly(True)
