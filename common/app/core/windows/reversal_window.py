from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from re import search
from typing import Optional
from logging import info
from common.app.forms.reversal import Ui_ReversalWindow
from common.app.constants.FilePath import FilePath
from common.app.core.tools.transaction import Transaction


class ReversalWindow(Ui_ReversalWindow, QDialog):
    _reversal_id: Optional[str] = None

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
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(FilePath.MAIN_LOGO))
        self.TransactionIdField.textEdited.connect(self.set_reversal_id)
        self.ComboBoxId.currentIndexChanged.connect(lambda index: self.id_item_changed())
        self.ComboBoxId.addItem("> Transaction queue")

        transaction: Transaction

        for transaction in transactions:
            item = "ID: %s | MTI: %s | UTRNNO: %s" % (
                transaction.trans_id,
                transaction.request.transaction.message_type_indicator,
                transaction.utrnno
            )

            self.ComboBoxId.addItem(item)

    def id_item_changed(self):
        value = search("ID:\s+?(\S+)", self.ComboBoxId.currentText())
        value = value.group(1) if value else value
        self.TransactionIdField.setText(str())
        self.TransactionIdField.setDisabled(bool(value))
        self.TransactionIdField.setText(value)
        self.set_reversal_id()

    def set_reversal_id(self):
        self.reversal_id = self.TransactionIdField.text()

    @staticmethod
    def get_reversal_id(id_list: list[Transaction] | None = None) -> str | None:
        window = ReversalWindow(id_list)
        result = window.exec_()

        if result == QDialog.Accepted:
            return window.reversal_id

        info("Reversal sending cancelled")
