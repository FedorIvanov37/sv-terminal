from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtGui import QPixmap, QIcon
from common.gui.constants import GuiFilesPath


class CheckableComboBox(QComboBox):
    _previous_text: str = ""

    def get_previous_text(self):
        return self._previous_text

    def mousePressEvent(self, e):
        self._previous_text = self.currentText()
        QComboBox.mousePressEvent(self, e)

    def addItem(self, item, state):
        super(CheckableComboBox, self).addItem(item)
        item = self.model().item(self.count() -1, 0)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        # item.setCheckState(state)

        if state == Qt.CheckState.Checked:
            item.setIcon(QIcon(QPixmap(GuiFilesPath.GREEN_CIRCLE)))
            return

        item.setIcon(QIcon())

    def itemChecked(self, index):
        item = self.model().item(index, 0)
        return item.checkState() == Qt.CheckState.Checked
