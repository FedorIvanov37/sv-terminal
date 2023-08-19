from sys import exit
from copy import deepcopy
from ctypes import windll
from pydantic import FilePath
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCloseEvent, QKeySequence, QShortcut, QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QMenu, QPushButton
from common.gui.core.JsonView import JsonView
from common.gui.forms.mainwindow import Ui_MainWindow
from common.gui.constants.ButtonActions import ButtonAction
from common.lib.constants.DataFormats import DataFormats
from common.gui.constants.ConnectionStatus import ConnectionDefinitions
from common.gui.constants.MainFieldSpec import MainFieldSpec as FieldsSpec
from common.gui.constants.GuiFilesPath import GuiFilesPath
from common.gui.decorators.window_settings import set_window_icon
from common.gui.constants.KeySequence import KeySequence
from common.lib.data_models.Transaction import TypeFields, Transaction
from common.lib.data_models.Config import Config


"""
MainWindow is a general SVTerminal GUI, Runs as an independent application, interacts with the backend using pyqtSignal 
Can be run separately from the backend, but does nothing in this case. 
 
The goals of MainWindow are interaction with the GUI user, user input data collection, and data processing requests 
using pyqtSignal. Better to not force it to process the data, validate values, and so on
"""


class MainWindow(Ui_MainWindow, QMainWindow):

    """
    Data processing request signals. Some of them send string modifiers as a hint on how to process the data
    Each signal has a corresponding @property for external interactions. The signals handling should be build
    using their properties
    """

    _window_close: pyqtSignal = pyqtSignal()
    _print: pyqtSignal = pyqtSignal(str)
    _save: pyqtSignal = pyqtSignal(str)
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
    _reset: pyqtSignal = pyqtSignal()
    _keep_alive: pyqtSignal = pyqtSignal(str)
    _repeat: pyqtSignal = pyqtSignal(str)
    _search_requested: pyqtSignal = pyqtSignal(str)

    @property
    def search_requested(self):
        return self._search_requested

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
    def json_view(self):
        return self._json_view

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

    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self._json_view: JsonView = JsonView(self.config)
        self._setup()

    @set_window_icon
    def _setup(self) -> None:
        self.setupUi(self)
        self._add_json_control_buttons()
        self._connect_all()
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("MainWindow")
        self.process_keep_alive_change(ButtonAction.KEEP_ALIVE_STOP)
        self.process_repeat_change(ButtonAction.KEEP_ALIVE_STOP)
        self.ButtonSend.setFocus()

    def _add_json_control_buttons(self) -> None:
        # Create and place the JSON-view control buttons as "New Field", "New Subfield", "Remove Field"

        self.FieldsTreeLayout.addWidget(self.json_view)
        self.PlusButton = QPushButton(ButtonAction.BUTTON_PLUS_SIGN)
        self.MinusButton = QPushButton(ButtonAction.BUTTON_MINUS_SIGN)
        self.NextLevelButton = QPushButton(ButtonAction.BUTTON_NEXT_LEVEL_SIGN)

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
        and so on. Call syntax is a little different for each group. One signal can be emitted by different methods,
        e.g. cause for transaction data sending (signal "send") can be MainWindow key press or keyboard key sequence.
        """

        buttons_connection_map = {  # Signals, which should be emitted by MainWindow key press event
            self.PlusButton: self.json_view.plus,
            self.MinusButton: self.json_view.minus,
            self.NextLevelButton: self.json_view.next_level,
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
            self.ButtonCopyBitmap: self.copy_bitmap,
        }

        json_view_connection_map = {
            self.json_view.itemChanged: self.field_changed,
            self.json_view.field_changed: self.field_changed,
            self.json_view.field_added: self.field_added,
            self.json_view.field_removed: self.field_removed,
            self.json_view.need_disable_next_level: self.disable_next_level_button,
            self.json_view.need_enable_next_level: self.enable_next_level_button,
        }

        other_connection_map = {
            self.SearchLine.textChanged: self.search_requested,
            self.search_requested: self.json_view.search,
        }

        keys_connection_map = {

            # Signals, which should be emitted by key sequences on keyboard
            # The string argument (modifier) is a hint about a requested data format

            # Predefined Key Sequences
            QKeySequence.StandardKey.New: self.json_view.plus,
            QKeySequence.StandardKey.Delete: self.json_view.minus,
            QKeySequence.StandardKey.HelpContents: self.about,
            QKeySequence.StandardKey.Print: self.ButtonPrintData.showMenu,
            QKeySequence.StandardKey.Save: self.ButtonSave.showMenu,
            QKeySequence.StandardKey.Open: self.parse_file,
            QKeySequence.StandardKey.Undo: self.json_view.undo,
            QKeySequence.StandardKey.Redo: self.json_view.redo,
            QKeySequence.StandardKey.Find: self.activate_search,

            # Custom Key Sequences
            # The string argument (modifier) is a hint about a requested data format
            KeySequence.CTRL_T: lambda: self.print.emit(DataFormats.TERM),
            KeySequence.CTRL_SHIFT_ENTER: lambda: self.reverse.emit(ButtonAction.LAST),
            KeySequence.CTRL_ENTER: self.send,
            KeySequence.CTRL_R: self.reconnect,
            KeySequence.CTRL_L: self.clear_log,
            KeySequence.CTRL_E: lambda: self.json_view.edit_column(FieldsSpec.ColumnsOrder.VALUE),
            KeySequence.CTRL_W: lambda: self.json_view.edit_column(FieldsSpec.ColumnsOrder.FIELD),
            KeySequence.CTRL_SHIFT_N: self.json_view.next_level,
            KeySequence.CTRL_ALT_Q: exit,
            KeySequence.CTRL_ALT_ENTER: self.echo_test,
        }

        self.buttons_menu_structure = {

            # Special menu buttons. Along with the signal they send modifiers - string values, aka pragma
            # The modifiers are used to define the requested data format or as a hint on how to process the data

            self.ButtonKeepAlive: {
                ButtonAction.KEEP_ALIVE_1S: lambda: self.keep_alive.emit(ButtonAction.KEEP_ALIVE_1S),
                ButtonAction.KEEP_ALIVE_5S: lambda: self.keep_alive.emit(ButtonAction.KEEP_ALIVE_5S),
                ButtonAction.KEEP_ALIVE_10S: lambda: self.keep_alive.emit(ButtonAction.KEEP_ALIVE_10S),
                ButtonAction.KEEP_ALIVE_30S: lambda: self.keep_alive.emit(ButtonAction.KEEP_ALIVE_30S),
                ButtonAction.KEEP_ALIVE_60S: lambda: self.keep_alive.emit(ButtonAction.KEEP_ALIVE_60S),
                ButtonAction.KEEP_ALIVE_300S: lambda: self.keep_alive.emit(ButtonAction.KEEP_ALIVE_300S),
                ButtonAction.KEEP_ALIVE_STOP: lambda: self.keep_alive.emit(ButtonAction.KEEP_ALIVE_STOP),
                ButtonAction.KEEP_ALIVE_ONCE: lambda: self.keep_alive.emit(ButtonAction.KEEP_ALIVE_ONCE),
            },

            self.ButtonRepeat: {
                ButtonAction.KEEP_ALIVE_1S: lambda: self.repeat.emit(ButtonAction.KEEP_ALIVE_1S),
                ButtonAction.KEEP_ALIVE_5S: lambda: self.repeat.emit(ButtonAction.KEEP_ALIVE_5S),
                ButtonAction.KEEP_ALIVE_10S: lambda: self.repeat.emit(ButtonAction.KEEP_ALIVE_10S),
                ButtonAction.KEEP_ALIVE_30S: lambda: self.repeat.emit(ButtonAction.KEEP_ALIVE_30S),
                ButtonAction.KEEP_ALIVE_60S: lambda: self.repeat.emit(ButtonAction.KEEP_ALIVE_60S),
                ButtonAction.KEEP_ALIVE_300S: lambda: self.repeat.emit(ButtonAction.KEEP_ALIVE_300S),
                ButtonAction.KEEP_ALIVE_STOP: lambda: self.repeat.emit(ButtonAction.KEEP_ALIVE_STOP),
            },

            self.ButtonReverse: {
                ButtonAction.LAST: lambda: self.reverse.emit(ButtonAction.LAST),
                ButtonAction.OTHER: lambda: self.reverse.emit(ButtonAction.OTHER),
            },

            self.ButtonPrintData: {
                DataFormats.DUMP: lambda: self.print.emit(DataFormats.DUMP),
                DataFormats.JSON: lambda: self.print.emit(DataFormats.JSON),
                DataFormats.INI: lambda: self.print.emit(DataFormats.INI),
                DataFormats.SPEC: lambda: self.print.emit(DataFormats.SPEC),
                DataFormats.TERM: lambda: self.print.emit(DataFormats.TERM),
            },

            self.ButtonSave: {
                DataFormats.JSON: lambda: self.save.emit(DataFormats.JSON),
                DataFormats.INI: lambda: self.save.emit(DataFormats.INI),
                DataFormats.DUMP: lambda: self.save.emit(DataFormats.DUMP),
            }
        }

        # The mapping is defined, let's connect them all

        for combination, function in keys_connection_map.items():  # Key sequences
            QShortcut(QKeySequence(combination), self).activated.connect(function)

        for button, slot in buttons_connection_map.items():
            button.clicked.connect(slot)

        for connection_map in json_view_connection_map, other_connection_map:  # Signals, activated by key press event
            for signal, slot in connection_map.items():
                signal.connect(slot)

        for button, actions in self.buttons_menu_structure.items():  # Menu buttons
            button.setMenu(QMenu())

            for action, function in actions.items():
                button.menu().addAction(action, function)
                button.menu().addSeparator()

    def activate_search(self):
        self.SearchLine.setFocus()

    def hide_secrets(self):
        self.json_view.hide_secrets()

    # Usually disables in fields flat-mode to avoid subfields creation
    def disable_next_level_button(self, disable: bool = True) -> None:
        self.NextLevelButton.setDisabled(disable)

    def enable_next_level_button(self, enable: bool = True) -> None:
        self.NextLevelButton.setEnabled(enable)

    # Switch from JSON mode to flat mode and back
    def set_json_mode(self, json_mode: bool) -> None:
        self.json_view.switch_json_mode(json_mode)

    # Validate whole transaction data, presented on MainWindow
    def validate_fields(self) -> None:
        self.json_view.validate_all()

    def clean_window_log(self) -> None:
        self.LogArea.setText(str())

    # Return transaction data fields in dict-representation
    def get_fields(self) -> TypeFields:
        return self.json_view.generate_fields()

    # Return fields list, no subfields included
    def get_top_level_field_numbers(self) -> list[str]:
        return self.json_view.get_top_level_field_numbers()

    def get_fields_to_generate(self) -> list[str]:
        return self.json_view.get_checkboxes()

    def get_mti(self, length: int = 4) -> str:
        message_type = self.msgtype.currentText()
        message_type = message_type[:length]
        return message_type

    def set_log_data(self, data: str = str()) -> None:
        self.LogArea.setText(data)

    def get_log_data(self) -> str:
        return self.LogArea.toPlainText()

    def get_bitmap_data(self) -> str:
        return self.Bitmap.text()

    # To avoid errors connection buttons will be disabled during the network connection opening
    def block_connection_buttons(self) -> None:
        self.change_connection_buttons_state(enabled=False)

    # After the connection status is changed connection buttons will be enabled again
    def unblock_connection_buttons(self) -> None:
        self.change_connection_buttons_state(enabled=True)

    def change_connection_buttons_state(self, enabled: bool) -> None:
        for button in (self.ButtonReconnect, self.ButtonSend, self.ButtonEchoTest, self.ButtonReverse):
            button.setEnabled(enabled)

    def set_mti_values(self, mti_list: list[str]):
        for mti in mti_list:
            self.msgtype.addItem(mti)

    # Get value of specific field
    def get_field_data(self, field_number: str) -> str:
        return self.json_view.get_field_data(field_number)

    # Set value of specific field
    def set_field_value(self, field, field_data) -> None:
        self.json_view.set_field_value(field, field_data)

    def set_mti_value(self, mti: str) -> None:
        index = self.msgtype.findText(mti, flags=Qt.MatchFlag.MatchContains)

        if index == -1:
            raise ValueError(f"Cannot set Message Type Identifier {mti}. Mti not in specification")

        self.msgtype.setCurrentIndex(index)

    def set_fields(self, transaction: Transaction) -> None:
        self.json_view.parse_transaction(transaction)
        self.set_bitmap()

    def clear_message(self) -> None:
        self.msgtype.setCurrentIndex(-1)
        self.json_view.clean()

    def set_connection_status(self, status) -> None:
        self.ConnectionStatusLabel.setPixmap(QPixmap(GuiFilesPath.GREEN_CIRCLE))
        self.ConnectionStatus.setText(ConnectionDefinitions.get_state_description(status))
        self.ConnectionStatusLabel.setPixmap(QPixmap(ConnectionDefinitions.get_state_icon_path(status)))

    def process_repeat_change(self, interval_name: str) -> None:
        icon_file: FilePath = GuiFilesPath.GREEN_CIRCLE

        if interval_name == ButtonAction.KEEP_ALIVE_STOP:
            icon_file: FilePath = GuiFilesPath.GREY_CIRCLE

        self.ButtonRepeat.setIcon(QIcon(QPixmap(icon_file)))
        self.ButtonRepeat.menu().clear()

        button_action_menu = deepcopy(self.buttons_menu_structure.get(self.ButtonRepeat))

        for action, function in button_action_menu.items():
            if action == interval_name:
                action = f"{ButtonAction.CURRENT_ACTION_MARK} {action}"  # Set checked

            self.ButtonRepeat.menu().addAction(action, function)
            self.ButtonRepeat.menu().addSeparator()

    # Change KeepAlive loop status
    def process_keep_alive_change(self, interval_name: str) -> None:
        if interval_name == ButtonAction.KEEP_ALIVE_ONCE:
            return

        icon_file: FilePath = GuiFilesPath.GREEN_CIRCLE

        if interval_name == ButtonAction.KEEP_ALIVE_STOP:
            icon_file: FilePath = GuiFilesPath.GREY_CIRCLE

        self.ButtonKeepAlive.setIcon(QIcon(QPixmap(icon_file)))
        self.ButtonKeepAlive.menu().clear()

        button_action_menu = deepcopy(self.buttons_menu_structure.get(self.ButtonKeepAlive))

        if self.config.smartvista.keep_alive_mode:  # Add custom interval
            interval: str = ButtonAction.KEEP_ALIVE_DEFAULT % self.config.smartvista.keep_alive_interval
            button_action_menu[interval] = lambda: self.keep_alive.emit(interval)

        for action, function in button_action_menu.items():
            if action == interval_name:
                action = f"{ButtonAction.CURRENT_ACTION_MARK} {action}"  # Set checked

            self.ButtonKeepAlive.menu().addAction(action, function)
            self.ButtonKeepAlive.menu().addSeparator()

    def set_bitmap(self, bitmap: str = str()) -> None:
        self.Bitmap.setText(bitmap)

    def closeEvent(self, a0: QCloseEvent) -> None:
        # Closing network connections and so on before MainWindow switch off
        self.hide()
        self.window_close.emit()
        a0.accept()
