from PyQt6.QtWidgets import QComboBox, QWidget
from PyQt6.QtGui import QFont
from signal.lib.core.EpaySpecification import EpaySpecification


class ComboBox(QComboBox):
    spec: EpaySpecification = EpaySpecification()

    def __init__(self, parent: QWidget | None = None):
        super(ComboBox, self).__init__(parent=parent)
        self._setup()

    def _setup(self):
        self.setFont(QFont("Calibri", 12))
        self.setEditable(False)
        self.addItems(self.spec.get_mti_list())
