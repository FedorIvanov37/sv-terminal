from re import search
from logging import error
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QTabWidget, QWidget, QGridLayout
from PyQt6.QtGui import QFont, QIcon
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
        self.config = config
        self._setup()
        self.connect_all()

    def _setup(self):
        self.setTabsClosable(True)
        self.setFont(QFont("Calibri", 12))
        self.add_tab()
        self.mark_active_tab()

    def connect_all(self):
        self.json_view.trans_id_set.connect(self.trans_id_set)
        self.tabBarDoubleClicked.connect(self.remove_tab)
        self.tabBarClicked.connect(self.process_tab_click)
        self.currentChanged.connect(self.process_tab_change)

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

    def remove_tab(self, index):
        if self.count() < 3:
            return

        self.removeTab(index)

    def process_tab_click(self, index):
        if index != self.count() - 1:
            self.mark_active_tab()
            return

        self.add_tab()
        self.mark_active_tab()
        self.new_tab_opened.emit()

    def process_tab_change(self):
        if self.count() < 3:
            self.setCurrentIndex(int())
            return

        if self.currentIndex() == self.count() - 1:
            self.setCurrentIndex(self.count() - 3)

        self.mark_active_tab()

    def mark_active_tab(self):
        grey_icon = QIcon(GuiFilesPath.GREY_CIRCLE)
        green_icon = QIcon(GuiFilesPath.GREEN_CIRCLE)

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
    def add_tab(self):
        if self.count() >= TabViewParams.TABS_LIMIT:
            error(f"Cannot open a new tab, max open tabs limit {TabViewParams.TABS_LIMIT} tabs is reached")
            error("Close some tab to open a new one")
            return

        self.close_tab(self.count() - 1)

        widget = QWidget()
        widget.setLayout(QGridLayout())
        widget.layout().addWidget(ComboBox(parent=widget))
        widget.layout().addWidget(LineEdit(parent=widget))
        widget.layout().addWidget(JsonView(self.config, parent=widget))

        self.addTab(widget, self.get_tab_name())
        # self.setTabIcon(self.count() - 1, QIcon(GuiFilesPath.GREEN_CIRCLE))
        self.setCurrentIndex(self.count() - 1)
        self.setTabsClosable(False)
        self.addTab(QWidget(), '+')

    def get_tab_name(self) -> str:
        tab_number: int = 1
        tab_name: str = "Tab #%s"

        if self.count() < 1:
            return tab_name % tab_number

        for index in range(self.count()):
            tab_text: str = self.tabText(index)

            try:
                tab_text: str = search(r"#\d+", tab_text).group(int())
            except AttributeError:
                return tab_name % tab_number

            tab_text: str = tab_text.replace("#", "")

            try:
                tab_text: int = int(tab_text) + 1
            except ValueError:
                return tab_name % tab_number

            if tab_text > tab_number:
                tab_number = tab_text

        return tab_name % tab_number

    def set_mti_value(self, mti: str) -> None:
        index = self.msg_type.findText(mti, flags=Qt.MatchFlag.MatchContains)

        if index == -1:
            raise ValueError(f"Cannot set Message Type Identifier {mti}. Mti not in specification")

        self.msg_type.setCurrentIndex(index)
