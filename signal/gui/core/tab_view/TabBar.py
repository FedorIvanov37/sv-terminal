from PyQt6.QtWidgets import QTabBar, QLineEdit


class TabBar(QTabBar):
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
        self.setTabText(self.__edited_tab, self.__edit.text())
        self.__edit.deleteLater()
