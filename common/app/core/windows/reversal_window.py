from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from re import search
from typing import Optional
from common.app.forms.reversal import Ui_ReversalWindow
from common.app.constants.FilePath import FilePath
from common.lib.data_models.Transaction import Transaction


class ReversalWindow(Ui_ReversalWindow, QDialog):
    _reversal_id: Optional[str] = None
    _accepted: bool = False

    @property
    def accepted(self):
        return self._accepted

    @accepted.setter
    def accepted(self, accepted):
        self._accepted = accepted

    @property
    def reversal_id(self):
        return self._reversal_id

    @reversal_id.setter
    def reversal_id(self, reversal_id):
        self._reversal_id = reversal_id

    def __init__(self, transactions: list[Transaction]):
        super().__init__()
        self.setupUi(self)
        self.setup(transactions)

    def setup(self, transactions: list[Transaction]) -> None:
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(FilePath.MAIN_LOGO))
        self.ComboBoxId.currentIndexChanged.connect(lambda index: self.id_item_changed())
        self.buttonBox.accepted.connect(self.set_reversal_id)
        self.ComboBoxId.addItem("> Transaction queue")

        for transaction in transactions:
            item = f"ID: {transaction.trans_id} | UTRNNO: {transaction.utrnno}"
            self.ComboBoxId.addItem(item)

    def id_item_changed(self):
        value = search("ID:\s+?(\S+)", self.ComboBoxId.currentText())
        value = value.group(1) if value else value
        self.TransactionIdField.setText(str())
        self.TransactionIdField.setDisabled(bool(value))
        self.TransactionIdField.setText(value)

    def set_reversal_id(self):
        self.reversal_id = self.TransactionIdField.text()
