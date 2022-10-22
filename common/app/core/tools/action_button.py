from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QPushButton


# Fix Qt bug


class ActionButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mouseMoveEvent(self, e: QMouseEvent):
        return
