from logging import error
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QTabWidget, QWidget, QGridLayout
from PyQt6.QtGui import QFont, QIcon
from signal.gui.core.tab_view.TabBar import TabBar
from signal.lib.data_models.Config import Config
from signal.gui.decorators.void_qt_signals import void_qt_signals
from signal.gui.core.json_views.JsonView import JsonView
from signal.gui.core.tab_view.ComboBox import ComboBox
from signal.gui.core.tab_view.LineEdit import LineEdit
from signal.lib.data_models.Transaction import Transaction
from signal.gui.enums.GuiFilesPath import GuiFilesPath
from signal.gui.enums.TabViewParams import TabViewParams


class TabView(QTabWidget):
    _field_changed: pyqtSignal = pyqtSignal()
    _field_removed: pyqtSignal = pyqtSignal()
    _field_added: pyqtSignal = pyqtSignal()
    _disable_next_level_button: pyqtSignal = pyqtSignal()
    _enable_next_level_button: pyqtSignal = pyqtSignal()
    _trans_id_set: pyqtSignal = pyqtSignal()
    _tab_changed: pyqtSignal = pyqtSignal()
    _new_tab_opened: pyqtSignal = pyqtSignal()

    @property
    def new_tab_opened(self):
        return self._new_tab_opened

    @property
    def tab_changed(self):
        return self._tab_changed

    @property
    def trans_id_set(self):
        return self._trans_id_set

    @property
    def disable_next_level_button(self):
        return self._disable_next_level_button

    @property
    def enable_next_level_button(self):
        return self._enable_next_level_button

    @property
    def field_changed(self):
        return self._field_changed

    @property
    def field_added(self):
        return self._field_added

    @property
    def field_removed(self):
        return self._field_removed

    @property
    def json_view(self):
        if not (json_view := self.tab_widget.findChild(JsonView)):
            return JsonView(self.config)

        return json_view

    @property
    def msg_type(self):
        return self.tab_widget.findChild(ComboBox)

    @property
    def bit_map(self):
        return self.tab_widget.findChild(LineEdit)

    @property
    def tab_widget(self):
        return self.currentWidget()

    def __init__(self, config: Config):
        super(QTabWidget, self).__init__()
        self.setTabBar(TabBar())
        self.config = config
        self._setup()
        self.connect_all()

    def _setup(self):
        self.setTabsClosable(False)
        self.setFont(QFont("Calibri", 12))

        try:
            self.add_tab(tab_name="Main")
        except IndexError:
            return

        self.mark_active_tab()

    def connect_all(self):
        self.tabBar().tabBarDoubleClicked.connect(self.tabBarDoubleClicked)
        self.json_view.trans_id_set.connect(self.trans_id_set)
        self.tabBarClicked.connect(self.process_tab_click)
        self.currentChanged.connect(self.process_tab_change)
        self.tabCloseRequested.connect(self.remove_tab)

        json_view_connection_map = {
            self.json_view.itemChanged: self.field_changed,
            self.json_view.field_changed: self.field_changed,
            self.json_view.field_added: self.field_added,
            self.json_view.field_removed: self.field_removed,
            self.json_view.need_disable_next_level: self.disable_next_level_button,
            self.json_view.need_enable_next_level: self.enable_next_level_button,
        }

        for signal, slot in json_view_connection_map.items():
            signal.connect(slot)

    def set_tab_name(self, tab_name, index=None):
        if index is None:
            index = self.currentIndex()

        self.setTabText(index, tab_name)

    def remove_tab(self, index):
        if self.count() < 3:
            return

        self.removeTab(index)
        self.setTabsClosable(not self.count() < 3)
        self.mark_active_tab()

    def process_tab_click(self, index):
        if index != self.count() - 1:
            self.mark_active_tab()
            return

        try:
            self.add_tab()
        except IndexError:
            return

        self.set_tab_non_closeable()
        self.new_tab_opened.emit()

    def set_tab_non_closeable(self, index=0):
        self.tabBar().tabButton(index, TabBar.ButtonPosition.RightSide).resize(int(), int())

    def process_tab_change(self):
        if self.count() < 3:
            self.setCurrentIndex(int())
            return

        if self.currentIndex() == self.count() - 1:
            self.setCurrentIndex(self.count() - 2)
            return

        self.mark_active_tab()

    def mark_active_tab(self):
        grey_icon = QIcon(GuiFilesPath.GREY_CIRCLE)
        green_icon = QIcon(GuiFilesPath.GREEN_CIRCLE)

        if self.count() <= 2:
            self.setTabIcon(int(), green_icon)
            return

        for tab_index in range(self.count() - 1):
            self.setTabIcon(tab_index, grey_icon)

        self.setTabIcon(self.currentIndex(), green_icon)

    def close_current_tab(self):
        if self.count() < 3:
            return

        self.close_tab(self.currentIndex())
        self.mark_active_tab()

    def prev_tab(self):
        self.setCurrentIndex(self.currentIndex() - 1)

    def next_tab(self):
        self.setCurrentIndex(self.currentIndex() + 1)

    def plus(self):
        self.json_view.plus()

    def minus(self):
        self.json_view.minus()

    def next_level(self):
        self.json_view.next_level()

    def close_tab(self, index: int):
        if self.count() < 2:
            return

        self.removeTab(index)

    def parse_fields(self, fields):
        self.json_view.clean()
        self.json_view.parse_fields(fields)

    def set_transaction_fields(self, transaction: Transaction, generate_trans_id: bool = True) -> None:
        self.json_view.parse_transaction(transaction, to_generate_trans_id=generate_trans_id)
        self.json_view.expandAll()
        self.json_view.resize_all()

    def clear_message(self) -> None:
        self.msg_type.setCurrentIndex(-1)
        self.json_view.clean()

    def set_json_focus(self):
        self.json_view.setFocus()

    @void_qt_signals
    def add_tab(self, tab_name=None, parse_default_file=True):
        if self.count() > TabViewParams.TABS_LIMIT:
            error(f"Cannot open a new tab, max open tabs limit {TabViewParams.TABS_LIMIT} tabs is reached")
            error("Close some tab to open a new one")

            raise IndexError

        self.close_tab(self.count() - 1)

        widget = QWidget()
        widget.setLayout(QGridLayout())
        widget.layout().addWidget(ComboBox(parent=widget))
        widget.layout().addWidget(LineEdit(parent=widget))
        widget.layout().addWidget(JsonView(self.config, parent=widget))

        self.addTab(widget, tab_name if tab_name else self.get_tab_name())

        if not parse_default_file:
            return

        self.add_plus_tab()

    def add_plus_tab(self):
        self.addTab(QWidget(), '')  # Add the technical "plus" tab
        self.setTabIcon(self.count() - 1, QIcon(GuiFilesPath.NEW_TAB))
        self.setTabsClosable(self.count() > 2)
        self.setCurrentIndex(self.count() - 2)

        try:
            self.tabBar().tabButton(self.count() - 1, TabBar.ButtonPosition.RightSide).resize(int(), int())
        except AttributeError:
            return

        self.mark_active_tab()

    def get_tab_name(self) -> str:
        tab_name_index = self.count()
        tab_name = f"Tab #{tab_name_index}"
        tab_names = [self.tabText(index) for index in range(self.count())]

        while tab_name in tab_names:
            tab_name_index += 1
            tab_name = f"Tab #{tab_name_index}"

        return tab_name

    def set_mti_value(self, mti: str) -> None:
        index = self.msg_type.findText(mti, flags=Qt.MatchFlag.MatchContains)

        if index == -1:
            raise ValueError(f"Cannot set Message Type Identifier {mti}. Mti not in specification")

        self.msg_type.setCurrentIndex(index)
