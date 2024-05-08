from sys import exit
from typing import Callable
from copy import deepcopy
from ctypes import windll
from pydantic import FilePath
from PyQt6.QtNetwork import QTcpSocket
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QCloseEvent, QKeySequence, QShortcut, QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QMenu, QPushButton
from common.gui.forms.mainwindow import Ui_MainWindow
from common.gui.decorators.window_settings import set_window_icon
from common.lib.data_models.Types import FieldPath
from common.lib.data_models.Config import Config
from common.gui.enums import ButtonActions, MainFieldSpec as FieldsSpec
from common.gui.enums.KeySequences import KeySequences
from common.gui.enums.GuiFilesPath import GuiFilesPath
from common.gui.enums.ConnectionStatus import ConnectionStatus, ConnectionIcon
from common.gui.enums.TabViewParams import TabViewParams
from common.lib.enums.DataFormats import OutputFilesFormat
from common.lib.enums import KeepAlive
from common.lib.enums.ReleaseDefinition import ReleaseDefinition
from common.lib.enums.TextConstants import TextConstants
from common.lib.core.EpaySpecification import EpaySpecification
from common.gui.core.tab_view.TabView import TabView


"""
MainWindow is a general SVTerminal GUI, Runs as an independent application, interacts with the backend using pyqtSignal 
Can be run separately from the backend, but does nothing in this case. 
 
The goals of MainWindow are interaction with the GUI user, user input data collection, and data processing requests 
using pyqtSignal. Better to not force it to process the data, validate values, and so on
"""


class MainWindow(Ui_MainWindow, QMainWindow):

    """
    Data processing request signals. Some of them send string modifiers as a hint on how to process the data
    Each common has a corresponding @property for external interactions. The signals handling should be build
    using their properties
    """

    _window_close: pyqtSignal = pyqtSignal()
    _print: pyqtSignal = pyqtSignal(str)
    _save: pyqtSignal = pyqtSignal(str, str)
    _reverse: pyqtSignal = pyqtSignal(str)
    _about: pyqtSignal = pyqtSignal()
    _field_changed: pyqtSignal = pyqtSignal()
    _field_removed: pyqtSignal = pyqtSignal()
    _field_added: pyqtSignal = pyqtSignal()
    _clear_log: pyqtSignal = pyqtSignal()
    _settings: pyqtSignal = pyqtSignal()
    _specification: pyqtSignal = pyqtSignal()
    _echo_test: pyqtSignal = pyqtSignal()
    _clear: pyqtSignal = pyqtSignal()
    _copy_log: pyqtSignal = pyqtSignal()
    _copy_bitmap: pyqtSignal = pyqtSignal()
    _reconnect: pyqtSignal = pyqtSignal()
    _parse_file: pyqtSignal = pyqtSignal()
    _hotkeys: pyqtSignal = pyqtSignal()
    _send: pyqtSignal = pyqtSignal()
    _reset: pyqtSignal = pyqtSignal(bool)
    _keep_alive: pyqtSignal = pyqtSignal(str)
    _repeat: pyqtSignal = pyqtSignal(str)
    _parse_complex_field: pyqtSignal = pyqtSignal()
    _validate_message: pyqtSignal = pyqtSignal(bool)
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    @property
    def json_view(self):
        return self._tab_view.json_view

    @property
    def tab_view(self):
        return self._tab_view

    @property
    def validate_message(self):
        return self._validate_message

    @property
    def repeat(self):
        return self._repeat

    @property
    def keep_alive(self):
        return self._keep_alive

    @property
    def field_added(self):
        return self._field_added

    @property
    def field_removed(self):
        return self._field_removed

    @property
    def log_browser(self):
        return self.LogArea

    @property
    def window_close(self):
        return self._window_close

    @property
    def send(self):
        return self._send

    @property
    def reset(self):
        return self._reset

    @property
    def clear_log(self):
        return self._clear_log

    @property
    def settings(self):
        return self._settings

    @property
    def specification(self):
        return self._specification

    @property
    def echo_test(self):
        return self._echo_test

    @property
    def clear(self):
        return self._clear

    @property
    def copy_log(self):
        return self._copy_log

    @property
    def copy_bitmap(self):
        return self._copy_bitmap

    @property
    def save(self):
        return self._save

    @property
    def reconnect(self):
        return self._reconnect

    @property
    def reverse(self):
        return self._reverse

    @property
    def print(self):
        return self._print

    @property
    def parse_file(self):
        return self._parse_file

    @property
    def hotkeys(self):
        return self._hotkeys

    @property
    def field_changed(self):
        return self._field_changed

    @property
    def about(self):
        return self._about

    @property
    def parse_complex_field(self):
        return self._parse_complex_field

    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self._tab_view: TabView = TabView(self.config)
        self._setup()

    @set_window_icon
    def _setup(self) -> None:
        self.setupUi(self)
        self._add_json_control_buttons()
        self._connect_all()
        self.setWindowTitle(f"{TextConstants.SYSTEM_NAME.capitalize()} {ReleaseDefinition.VERSION}")
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("MainWindow")
        self.ButtonSend.setFocus()
        self.set_connection_status(QTcpSocket.SocketState.UnconnectedState)

        for trans_type in KeepAlive.TransTypes.TRANS_TYPE_KEEP_ALIVE, KeepAlive.TransTypes.TRANS_TYPE_TRANSACTION:
            self.process_transaction_loop_change(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_STOP, trans_type)

        self.TabViewLayout.addWidget(self._tab_view)

    def _add_json_control_buttons(self) -> None:
        # Create and place the JSON-view control buttons as "New Field", "New Subfield", "Remove Field"

        self.PlusButton = QPushButton(ButtonActions.ButtonActionSigns.BUTTON_PLUS_SIGN)
        self.MinusButton = QPushButton(ButtonActions.ButtonActionSigns.BUTTON_MINUS_SIGN)
        self.NextLevelButton = QPushButton(ButtonActions.ButtonActionSigns.BUTTON_NEXT_LEVEL_SIGN)

        buttons_layouts_map = {
            self.PlusLayout: self.PlusButton,
            self.MinusLayout: self.MinusButton,
            self.NextLevelLayout: self.NextLevelButton
        }

        for layout, button in buttons_layouts_map.items():
            layout.addWidget(button)

    def _connect_all(self) -> None:
        """
        This function connects buttons, key sequences, and special menu buttons to corresponding data processing
        requests. The MainWindow doesn't process the data by itself, instead of this it will send a data processing
        request by pyqtSignal. All of these groups use the same signals - clear, echo_test, parse_file, reconnect,
        and so on. Call syntax is a little different for each group. One common can be emitted by different methods,
        e.g. cause for transaction data sending (common "send") can be MainWindow key press or keyboard key sequence.
        """

        buttons_connection_map = {  # Signals, which should be emitted by MainWindow key press event
            self.PlusButton: self._tab_view.plus,
            self.MinusButton: self._tab_view.minus,
            self.NextLevelButton: self._tab_view.next_level,
            self.ButtonSend: self.send,
            self.ButtonClearLog: self.clear_log,
            self.ButtonCopyLog: self.copy_log,
            self.ButtonParseDump: self.parse_file,
            self.ButtonClearMessage: self.clear,
            self.ButtonDefault: self.reset,
            self.ButtonEchoTest: self.echo_test,
            self.ButtonReconnect: self.reconnect,
            self.ButtonSpecification: self.specification,
            self.ButtonHotkeys: self.hotkeys,
            self.ButtonSettings: self.settings,
            self.ButtonFieldsParser: self.parse_complex_field,
            self.ButtonValidate: lambda: self.validate_message.emit(True),
        }

        tab_view_connection_map = {
            self._tab_view.field_changed: self.field_changed,
            self._tab_view.field_added: self.field_added,
            self._tab_view.field_removed: self.field_removed,
            self._tab_view.disable_next_level_button: self.disable_next_level_button,
            self._tab_view.enable_next_level_button: self.enable_next_level_button,
            self._tab_view.new_tab_opened: lambda: self.reset.emit(False),
            self._tab_view.copy_bitmap: self.copy_bitmap,
            self._tab_view.trans_id_set: self.set_reversal_trans_id,
            self._tab_view.tab_changed: self.process_tab_change,
        }

        main_window_connection_map = {
            self.SearchLine.textChanged: self.search,
            self.SearchLine.editingFinished: self._tab_view.set_json_focus,
        }

        keys_connection_map = {

            # Signals, which should be emitted by key sequences on keyboard
            # The string argument (modifier) is a hint about a requested data format

            # Predefined Key Sequences
            QKeySequence.StandardKey.New: self._tab_view.plus,
            QKeySequence.StandardKey.Delete: self._tab_view.minus,
            QKeySequence.StandardKey.HelpContents: self.about,
            QKeySequence.StandardKey.Print: self.ButtonPrintData.showMenu,
            QKeySequence.StandardKey.Save: self.ButtonSave.showMenu,
            QKeySequence.StandardKey.Open: self.parse_file,
            QKeySequence.StandardKey.Undo: self.json_view.undo,
            QKeySequence.StandardKey.Redo: self.json_view.redo,
            QKeySequence.StandardKey.Find: self.activate_search,
            QKeySequence.StandardKey.Close: self._tab_view.close_current_tab,

            # Custom Key Sequences
            # The string argument (modifier) is a hint about a requested data format
            KeySequences.CTRL_T: self.add_tab,
            KeySequences.CTRL_SHIFT_ENTER: lambda: self.reverse.emit(ButtonActions.ReversalMenuActions.LAST),
            KeySequences.CTRL_ENTER: self.send,
            KeySequences.CTRL_R: self.reconnect,
            KeySequences.CTRL_L: self.clear_log,
            KeySequences.CTRL_E: lambda: self.json_view.edit_column(FieldsSpec.ColumnsOrder.VALUE),
            KeySequences.CTRL_W: lambda: self.json_view.edit_column(FieldsSpec.ColumnsOrder.FIELD),
            KeySequences.CTRL_Q: self._tab_view.close_current_tab,
            KeySequences.CTRL_SHIFT_N: self._tab_view.next_level,
            KeySequences.CTRL_ALT_Q: exit,
            KeySequences.CTRL_ALT_ENTER: self.echo_test,
            KeySequences.CTRL_ALT_V: lambda: self.validate_message.emit(True),
            KeySequences.CTRL_PAGE_UP: self._tab_view.prev_tab,
            KeySequences.CTRL_PAGE_DOWN: self._tab_view.next_tab,
            KeySequences.CTRL_TAB: self._tab_view.next_tab,
            KeySequences.CTRL_SHIFT_TAB: self._tab_view.prev_tab,
            KeySequences.CTRL_ALT_P: lambda: self.print.emit(ButtonActions.PrintButtonDataFormats.TERM),

        }

        self.buttons_menu_structure = {

            # Special menu buttons. Along with the common they send modifiers - string values, aka pragma
            # The modifiers are used to define the requested data format or as a hint on how to process the data

            self.ButtonKeepAlive: {
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_1S: lambda: self.keep_alive.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_1S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_5S: lambda: self.keep_alive.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_5S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_10S: lambda: self.keep_alive.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_10S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_30S: lambda: self.keep_alive.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_30S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_60S: lambda: self.keep_alive.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_60S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_300S: lambda: self.keep_alive.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_300S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_STOP: lambda: self.keep_alive.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_STOP),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_ONCE: lambda: self.keep_alive.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_ONCE),
            },

            self.ButtonRepeat: {
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_1S: lambda: self.repeat.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_1S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_5S: lambda: self.repeat.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_5S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_10S: lambda: self.repeat.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_10S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_30S: lambda: self.repeat.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_30S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_60S: lambda: self.repeat.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_60S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_300S: lambda: self.repeat.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_300S),
                ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_STOP: lambda: self.repeat.emit(ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_STOP),
            },

            self.ButtonReverse: {
                ButtonActions.ReversalMenuActions.LAST: lambda: self.reverse.emit(ButtonActions.ReversalMenuActions.LAST),
                ButtonActions.ReversalMenuActions.OTHER: lambda: self.reverse.emit(ButtonActions.ReversalMenuActions.OTHER),
                ButtonActions.ReversalMenuActions.SET_REVERSAL: lambda: self.reverse.emit(ButtonActions.ReversalMenuActions.SET_REVERSAL),
            },

            self.ButtonPrintData: {
                ButtonActions.PrintButtonDataFormats.DUMP: lambda: self.print.emit(ButtonActions.PrintButtonDataFormats.DUMP),
                ButtonActions.PrintButtonDataFormats.JSON: lambda: self.print.emit(ButtonActions.PrintButtonDataFormats.JSON),
                ButtonActions.PrintButtonDataFormats.INI: lambda: self.print.emit(ButtonActions.PrintButtonDataFormats.INI),
                ButtonActions.PrintButtonDataFormats.SPEC: lambda: self.print.emit(ButtonActions.PrintButtonDataFormats.SPEC),
                ButtonActions.PrintButtonDataFormats.TERM: lambda: self.print.emit(ButtonActions.PrintButtonDataFormats.TERM),
                ButtonActions.PrintButtonDataFormats.CONFIG: lambda: self.print.emit(ButtonActions.PrintButtonDataFormats.CONFIG),
            },

            self.ButtonSave: {
                ButtonActions.SaveMenuActions.CURRENT_TAB: lambda: self.save.emit(ButtonActions.SaveMenuActions.CURRENT_TAB, str()),
            }
        }

        # The mapping is defined, let's connect them all

        for combination, function in keys_connection_map.items():  # Key sequences
            QShortcut(QKeySequence(combination), self).activated.connect(function)

        for button, slot in buttons_connection_map.items():
            button.clicked.connect(slot)

        for connection_map in tab_view_connection_map, main_window_connection_map:  # Signals, activated by key event
            for signal, slot in connection_map.items():
                signal.connect(slot)

        for button, actions in self.buttons_menu_structure.items():  # Menu buttons
            button.setMenu(QMenu())

            for action, function in actions.items():
                button.menu().addAction(action, function)
                button.menu().addSeparator()

        self.ButtonSave.menu().addMenu(ButtonActions.SaveMenuActions.ALL_TABS)

        self.ButtonSave.menu().findChild(QMenu).addAction(OutputFilesFormat.JSON, lambda: self.save.emit(
            ButtonActions.SaveMenuActions.ALL_TABS, OutputFilesFormat.JSON))

        self.ButtonSave.menu().findChild(QMenu).addAction(OutputFilesFormat.INI, lambda: self.save.emit(
            ButtonActions.SaveMenuActions.ALL_TABS, OutputFilesFormat.INI))

        self.ButtonSave.menu().findChild(QMenu).addAction(OutputFilesFormat.DUMP, lambda: self.save.emit(
            ButtonActions.SaveMenuActions.ALL_TABS, OutputFilesFormat.DUMP))

    def set_tab_name(self, tab_name):
        self._tab_view.set_tab_name(tab_name)

    def add_tab(self):
        try:
            self._tab_view.add_tab()
        except IndexError:
            return

        self.reset.emit(False)

    def search(self, text):
        self.json_view.search(text)

    def process_tab_change(self):
        self.SearchLine.setText(str())
        self.json_view.search(str())
        self.json_view.expandAll()

    def is_json_mode_on(self, field_path: FieldPath):
        return self.json_view.is_json_mode_on(field_path)

    def set_reversal_trans_id(self):
        if not (trans_id := self.json_view.get_trans_id()):
            return

        if not self.spec.is_reversal(self.get_mti()):
            return

        if not self.json_view.is_trans_id_generate_mode_on():
            return

        self.json_view.set_trans_id(f"{trans_id}_R")

    def set_focus(self):
        self.json_view.setFocus()

    def activate_search(self):
        self.SearchLine.setFocus()

    # Usually disables in fields flat-mode to avoid subfields creation
    def disable_next_level_button(self, disable: bool = True) -> None:
        self.NextLevelButton.setDisabled(disable)

    def enable_next_level_button(self, enable: bool = True) -> None:
        self.NextLevelButton.setEnabled(enable)

    def get_tab_names(self, all_tabs: bool = False) -> list[str]:
        if all_tabs:
            return self._tab_view.get_tab_names()

        if not self._tab_view.get_current_tab_name():
            self._tab_view.set_tab_name()

        return [self._tab_view.get_current_tab_name()]

    def parse_tab(self, tab_name: str = None, flat=False):
        if tab_name is None:
            tab_name = TabViewParams.MAIN_TAB_NAME

        return self._tab_view.generate_fields(tab_name, flat=flat)

    def get_trans_id(self, tab_name: str):
        return self._tab_view.get_trans_id(tab_name)

    # Validate whole transaction data, presented on MainWindow
    def validate_fields(self, force=False) -> None:
        self.json_view.check_all_items(force=force)

    def clean_window_log(self) -> None:
        self.LogArea.setText(str())

    def get_fields_to_generate(self) -> list[str]:
        return self.json_view.get_checkboxes()

    def get_mti(self, length: int = 4, tab_name: str | None = None) -> str | None:
        if tab_name is None and not (tab_name := self._tab_view.get_current_tab_name()):
            self._tab_view.set_tab_name()

        if not self._tab_view.get_current_tab_name():
            raise ValueError("Lost tab name")

        if not (msg_type_box := self._tab_view.get_msg_type(tab_name)):
            return

        if not (message_type := msg_type_box.currentText()):
            return

        if not (message_type := message_type[:length]):
            return

        return message_type

    def set_log_data(self, data: str = str()) -> None:
        self.LogArea.setText(data)

    def get_log_data(self) -> str:
        return self.LogArea.toPlainText()

    def get_bitmap_data(self) -> str:
        return self._tab_view.bit_map.text()

    # To avoid errors connection buttons will be disabled during the network connection opening
    def block_connection_buttons(self) -> None:
        self.change_connection_buttons_state(enabled=False)

    # After the connection status is changed connection buttons will be enabled again
    def unblock_connection_buttons(self) -> None:
        self.change_connection_buttons_state(enabled=True)

    def change_connection_buttons_state(self, enabled: bool) -> None:
        for button in (self.ButtonReconnect, self.ButtonSend, self.ButtonEchoTest, self.ButtonReverse):
            button.setEnabled(enabled)

    def set_connection_status(self, status: QTcpSocket.SocketState) -> None:
        try:
            text = ConnectionStatus[status.name]
            icon = ConnectionIcon[status.name]

        except KeyError:
            text = ConnectionStatus.ConnectionStatuses.UNKNOWN
            icon = ConnectionStatus.ConnectionIcons.GREY

        self.ConnectionStatus.setText(text)
        self.ConnectionStatusLabel.setPixmap(QPixmap(icon))

    def process_transaction_loop_change(self, interval_name: str, trans_type: str):
        if interval_name == ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_ONCE:
            return

        button_type_map: dict[str, QPushButton] = {
            KeepAlive.TransTypes.TRANS_TYPE_KEEP_ALIVE: self.ButtonKeepAlive,
            KeepAlive.TransTypes.TRANS_TYPE_TRANSACTION: self.ButtonRepeat,
        }

        if not (button := button_type_map.get(trans_type)):
            return

        button_action_menu: dict[str, Callable] = deepcopy(self.buttons_menu_structure.get(button))

        icon_file: FilePath = GuiFilesPath.GREEN_CIRCLE

        if interval_name == ButtonActions.KeepAliveTimeIntervals.KEEP_ALIVE_STOP:
            icon_file: FilePath = GuiFilesPath.GREY_CIRCLE

        button.setIcon(QIcon(QPixmap(icon_file)))
        button.menu().clear()

        if trans_type == KeepAlive.TransTypes.TRANS_TYPE_KEEP_ALIVE and self.config.host.keep_alive_mode:
            custom_interval_name: str = KeepAlive.IntervalNames.KEEP_ALIVE_DEFAULT % self.config.host.keep_alive_interval

            button_action_menu[custom_interval_name]: Callable = lambda: self.keep_alive.emit(custom_interval_name)

        for action, function in button_action_menu.items():
            if action == interval_name:
                action: str = f"{ButtonActions.Marks.CURRENT_ACTION_MARK} {action}"  # Set checked

            button.menu().addAction(action, function)
            button.menu().addSeparator()

    def set_bitmap(self, bitmap: str = str()) -> None:
        self._tab_view.bit_map.setText(bitmap)

    def closeEvent(self, a0: QCloseEvent) -> None:
        # Closing network connections and so on before MainWindow switch off
        self.hide()
        self.window_close.emit()
        a0.accept()
