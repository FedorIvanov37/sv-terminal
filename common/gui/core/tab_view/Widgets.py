from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QTabBar, QComboBox, QWidget, QLineEdit, QPushButton
from common.lib.core.EpaySpecification import EpaySpecification


FONT: QFont = QFont("Calibri", 12)


class PushButton(QPushButton):
    def __init__(self, parent: QWidget | None = None):
        super(PushButton, self).__init__(parent=parent)
        self._setup()

    def _setup(self):
        self.setFont(QFont("MS Shell Dlg 2", 10))
        self.setText("Copy")
        self.setFixedSize(75, 27)


class ComboBox(QComboBox):
    spec: EpaySpecification = EpaySpecification()

    def __init__(self, parent: QWidget | None = None):
        super(ComboBox, self).__init__(parent=parent)
        self._setup()

    def _setup(self):
        self.setFont(FONT)
        self.setEditable(False)
        self.addItems(self.spec.get_mti_list())


class LineEdit(QLineEdit):
    def __init__(self, parent: QWidget | None = None):
        super(LineEdit, self).__init__(parent=parent)
        self._setup()

    def _setup(self):
        self.setFont(FONT)
        self.setReadOnly(True)


class TabBar(QTabBar):
    _text_edited: pyqtSignal = pyqtSignal(int, str)  # Tab index, new text

    @property
    def text_edited(self):
        return self._text_edited

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(False)

    def mouseDoubleClickEvent(self, event):
        tab_index = self.tabAt(event.pos())

        if tab_index == int():
            return

        self.tabBarDoubleClicked.emit(tab_index)
        self.start_rename(tab_index)

    def start_rename(self, tab_index):
        self.__edited_tab = tab_index
        rect = self.tabRect(tab_index)
        top_margin = 3
        left_margin = 6
        self.__edit = QLineEdit(self)
        self.__edit.show()
        self.__edit.move(rect.left() + left_margin, rect.top() + top_margin)
        self.__edit.resize(rect.width() - 2 * left_margin, rect.height() - 2 * top_margin)
        self.__edit.setText(self.tabText(tab_index))
        self.__edit.selectAll()
        self.__edit.setFocus()
        self.__edit.editingFinished.connect(self.finish_rename)

    def finish_rename(self):
        self.text_edited.emit(self.__edited_tab, self.__edit.text())
        self.__edit.deleteLater()
