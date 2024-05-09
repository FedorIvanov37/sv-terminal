from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QTabBar, QComboBox, QWidget, QLineEdit, QPushButton
from common.lib.core.EpaySpecification import EpaySpecification


CALIBRI_12: QFont = QFont("Calibri", 12)
MS_SHELL_10: QFont = QFont("MS Shell Dlg 2", 10)


class PushButton(QPushButton):
    def __init__(self, parent: QWidget | None = None):
        super(PushButton, self).__init__(parent=parent)
        self._setup()

    def _setup(self):
        self.setFont(MS_SHELL_10)
        self.setText("Copy")
        self.setFixedSize(75, 27)


class ComboBox(QComboBox):
    spec: EpaySpecification = EpaySpecification()

    def __init__(self, parent: QWidget | None = None):
        super(ComboBox, self).__init__(parent=parent)
        self._setup()

    def _setup(self):
        self.setFont(CALIBRI_12)
        self.setEditable(False)
        self.addItems(self.spec.get_mti_list())


class LineEdit(QLineEdit):
    def __init__(self, parent: QWidget | None = None):
        super(LineEdit, self).__init__(parent=parent)
        self._setup()

    def _setup(self):
        self.setFont(CALIBRI_12)
        self.setReadOnly(True)


class TabBar(QTabBar):
    # Custom TabBar
    # Allows to edit tab names and signals about the tab name change

    _text_edited: pyqtSignal = pyqtSignal(int, str)  # Tab index, new text
    _edited_tab: int
    _edit: QLineEdit

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
        top_margin = 3
        left_margin = 6
        rect = self.tabRect(tab_index)
        self._edited_tab = tab_index
        self._edit = QLineEdit(self)
        self._edit.show()
        self._edit.move(rect.left() + left_margin, rect.top() + top_margin)
        self._edit.resize(rect.width() - 2 * left_margin, rect.height() - 2 * top_margin)
        self._edit.setText(self.tabText(tab_index))
        self._edit.selectAll()
        self._edit.setFocus()
        self._edit.editingFinished.connect(self.finish_rename)

    def finish_rename(self):
        self.text_edited.emit(self._edited_tab, self._edit.text())
        self._edit.deleteLater()
