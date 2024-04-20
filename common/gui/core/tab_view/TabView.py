from logging import error, info
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon
from common.gui.core.tab_view.Widgets import TabBar, ComboBox, LineEdit, PushButton
from common.lib.data_models.Config import Config
from common.gui.decorators.void_qt_signals import void_qt_signals
from common.gui.core.json_views.JsonView import JsonView
from common.lib.data_models.Transaction import Transaction
from common.gui.enums.GuiFilesPath import GuiFilesPath
from common.gui.enums.TabViewParams import TabViewParams
from common.gui.core.json_items import FIeldItem


class TabView(QTabWidget):
    _field_changed: pyqtSignal = pyqtSignal()
    _field_removed: pyqtSignal = pyqtSignal()
    _field_added: pyqtSignal = pyqtSignal()
    _disable_next_level_button: pyqtSignal = pyqtSignal()
    _enable_next_level_button: pyqtSignal = pyqtSignal()
    _trans_id_set: pyqtSignal = pyqtSignal()
    _tab_changed: pyqtSignal = pyqtSignal()
    _new_tab_opened: pyqtSignal = pyqtSignal()
    _copy_bitmap: pyqtSignal = pyqtSignal()

    @property
    def copy_bitmap(self):
        return self._copy_bitmap

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
        self.json_view.trans_id_set.connect(self.trans_id_set)
        self.tabBarClicked.connect(self.process_tab_click)
        self.currentChanged.connect(self.process_tab_change)
        self.tabCloseRequested.connect(self.remove_tab)

    def connect_json_view(self):
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
        try:
            self.tabBar().tabButton(index, TabBar.ButtonPosition.RightSide).resize(int(), int())
        except AttributeError:
            return

    def process_tab_change(self):
        self.tab_changed.emit()

        if self.count() < 3:
            self.setCurrentIndex(int())
            return

        if self.currentIndex() == self.count() - 1:
            self.setCurrentIndex(int())
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

        if self.currentIndex() == int():
            return

        self.close_tab(self.currentIndex())
        self.prev_tab()
        self.mark_active_tab()

    def prev_tab(self):
        if self.currentIndex() == int():
            self.setCurrentIndex(self.count() - 2)
            return

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
    def add_tab(self, tab_name=None):
        if self.count() > int(TabViewParams.TABS_LIMIT):
            error(f"Cannot open a new tab, max open tabs limit {TabViewParams.TABS_LIMIT} tabs is reached")
            error("Close some tab to open a new one")

            raise IndexError

        self.close_tab(self.count() - 1)

        widget = self.generate_tab_widget()

        self.addTab(widget, tab_name if tab_name else self.get_tab_name())
        self.add_plus_tab()
        self.set_tab_non_closeable()
        self.connect_json_view()

    def generate_tab_widget(self):
        widget = QWidget()
        button = PushButton(parent=widget)

        bitmap_layout = QHBoxLayout()
        bitmap_layout.addWidget(LineEdit())
        bitmap_layout.addWidget(button)

        widget.setLayout(QVBoxLayout())

        widget.layout().addWidget(ComboBox(parent=widget))
        widget.layout().insertLayout(1, bitmap_layout)
        widget.layout().addWidget(JsonView(self.config, parent=widget))

        button.clicked.connect(self.copy_bitmap)

        return widget

    def copy_bitmap_pressed(self):
        self.copy_bitmap.emit()
        info("Bitmap copied")

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

    def get_tab_names(self) -> list[str]:
        tab_names: list[str] = list()

        for index in range(self.count() - 1):
            tab_name = self.tabText(index)

            if not tab_name.strip():
                tab_name = f"Tab #{index}"

            while tab_name in tab_names:
                tab_name = f"{index}_{tab_name}"

            self.setTabText(index, tab_name)

            tab_names.append(tab_name)

        return tab_names

    def get_tab_by_name(self, tab_name: str) -> QWidget | None:
        if tab_name not in self.get_tab_names():
            return

        for index in range(self.count()):
            if self.tabText(index) != tab_name:
                continue

            if not (tab := self.widget(index)):
                return

            return tab

    def get_json_view(self, tab_name) -> JsonView | None:
        if not (tab := self.get_tab_by_name(tab_name)):
            return

        if not (json_view := tab.findChild(JsonView)):
            return

        return json_view

    def generate_fields(self, tab_name: str, flat: bool = False):
        fields = {}

        if not (json_view := self.get_json_view(tab_name)):
            return fields

        if fields := json_view.generate_fields(flat=flat):
            return fields

        return fields

    def get_msg_type(self, tab_name):
        if not (tab := self.get_tab_by_name(tab_name)):
            return

        if not (msg_type := tab.findChild(ComboBox)):
            return

        return msg_type

    def get_trans_id(self, tab_name) -> str | None:
        if not (json_view := self.get_json_view(tab_name)):
            return

        return json_view.get_trans_id()

    def get_current_tab_name(self):
        return self.tabText(self.currentIndex())

    def get_current_field_data(self) -> str | None:
        field_item: FIeldItem

        if not (field_item := self.json_view.currentItem()):
            return

        return field_item.field_data
