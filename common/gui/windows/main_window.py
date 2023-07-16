from ctypes import windll
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QCloseEvent
from PyQt6.QtWidgets import QMainWindow, QMenu, QPushButton
from common.gui.forms.mainwindow import Ui_MainWindow
from common.gui.constants.ButtonActions import ButtonAction
from common.gui.constants.DataFormats import DataFormats
from common.gui.constants.ConnectionStatus import ConnectionDefinitions
from common.gui.constants.MainFieldSpec import MainFieldSpec as FieldsSpec
from common.gui.core.JsonView import JsonView
from common.lib.data_models.Transaction import TypeFields, Transaction
from common.lib.data_models.Config import Config
from PyQt6.QtGui import QKeySequence, QShortcut
from common.gui.decorators.window_settings import set_window_icon
from sys import exit


class MainWindow(Ui_MainWindow, QMainWindow):
    _json_view: JsonView
    _window_close: pyqtSignal = pyqtSignal()
    _print: pyqtSignal = pyqtSignal(str)
    _save: pyqtSignal = pyqtSignal(str)
    _reverse: pyqtSignal = pyqtSignal(str)
    _about: pyqtSignal = pyqtSignal()
    _field_changed: pyqtSignal = pyqtSignal()
    _field_removed: pyqtSignal = pyqtSignal()
    _field_added: pyqtSignal = pyqtSignal()
    #
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
    #
    @property
    def clear_log(self):
        return self._clear_log
    #
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
    def _setup(self):
        self.setupUi(self)

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

        self.connect_all()

        windll.shell32.SetCurrentProcessExplicitAppUserModelID("MainWindow")

    def connect_all(self):
        buttons_connection_map = {
            self.PlusButton.clicked: self.json_view.plus,
            self.MinusButton.clicked: self.json_view.minus,
            self.NextLevelButton.clicked: self.json_view.next_level,
            self.json_view.itemChanged: self.field_changed,
            self.json_view.field_added: self.field_added,
            self.json_view.field_removed: self.field_removed,
            self.ButtonSend.clicked: self.send,
            self.ButtonClearLog.clicked: self.clear_log,
            self.ButtonCopyLog.clicked: self.copy_log,
            self.ButtonParseDump.clicked: self.parse_file,
            self.ButtonClearMessage.clicked: self.clear,
            self.ButtonDefault.clicked: self.reset,
            self.ButtonEchoTest.clicked: self.echo_test,
            self.ButtonReconnect.clicked: self.reconnect,
            self.ButtonSpecification.clicked: self.specification,
            self.ButtonHotkeys.clicked: self.hotkeys,
            self.ButtonSettings.clicked: self.settings,
            self.ButtonCopyBitmap.clicked: self.copy_bitmap,
        }

        keys_connection_map = {
            'Ctrl+T': lambda: self.print.emit(DataFormats.TERM),
            'Ctrl+Shift+Return': lambda: self.reverse.emit(ButtonAction.LAST),
            'Ctrl+Return': self.send,
            'Ctrl+R': self.reconnect,
            'Ctrl+L': self.clear_log,
            'Ctrl+E': lambda: self.json_view.edit_column(FieldsSpec.ColumnsOrder.VALUE),
            'Ctrl+W': lambda: self.json_view.edit_column(FieldsSpec.ColumnsOrder.FIELD),
            'Ctrl+Shift+N': self.json_view.next_level,
            'Ctrl+Alt+Q': exit,
            'Ctrl+Alt+Return': self.echo_test,
            QKeySequence.StandardKey.New: self.json_view.plus,
            QKeySequence.StandardKey.Delete: self.json_view.minus,
            QKeySequence.StandardKey.HelpContents: self.about,
            QKeySequence.StandardKey.Save: self.ButtonSave.showMenu,
            QKeySequence.StandardKey.Print: self.ButtonPrintData.showMenu,
            QKeySequence.StandardKey.Open: self.parse_file,
        }

        buttons_menu_structure = {
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

        for signal, slot in buttons_connection_map.items():
            signal.connect(slot)

        for combination, function in keys_connection_map.items():
            QShortcut(QKeySequence(combination), self).activated.connect(function)

        for button, actions in buttons_menu_structure.items():
            button.setMenu(QMenu())

            for action, function in actions.items():
                button.menu().addAction(action, function)
                button.menu().addSeparator()

    def clean_window_log(self):
        self.LogArea.setText(str())

    def get_fields(self) -> TypeFields:
        return self.json_view.generate_fields()

    def get_top_level_field_numbers(self):
        return self.json_view.get_top_level_field_numbers()

    def get_fields_to_generate(self):
        return self.json_view.get_checkboxes()

    def get_mti(self, length=4):
        message_type = self.msgtype.currentText()
        message_type = message_type[:length]
        return message_type

    def set_log_data(self, data: str = str()):
        self.LogArea.setText(data)

    def get_log_data(self) -> str:
        return self.LogArea.toPlainText()

    def get_bitmap_data(self) -> str:
        return self.Bitmap.text()

    def block_connection_buttons(self):
        self.change_connection_buttons_state(enabled=False)

    def unblock_connection_buttons(self):
        self.change_connection_buttons_state(enabled=True)

    def change_connection_buttons_state(self, enabled: bool):
        for button in (self.ButtonReconnect, self.ButtonSend, self.ButtonEchoTest, self.ButtonReverse):
            button.setEnabled(enabled)

    def set_mti_values(self, mti_list: list[str]):
        for mti in mti_list:
            self.msgtype.addItem(mti)

    def get_field_data(self, field_number: str):
        return self.json_view.get_field_data(field_number)

    def set_mti_value(self, mti: str):
        index = self.msgtype.findText(mti, flags=Qt.MatchFlag.MatchContains)

        if index == -1:
            raise ValueError(f"Cannot set Message Type Identifier {mti}. Mti not in specification")

        self.msgtype.setCurrentIndex(index)

    def set_fields(self, transaction: Transaction):
        self.json_view.parse_transaction(transaction)
        self.set_bitmap()

    def set_field_value(self, field, field_data):
        self.json_view.set_field_value(field, field_data)

    def clear_message(self):
        self.msgtype.setCurrentIndex(-1)
        self.json_view.clean()

    def set_connection_status(self, status):
        self.ConnectionStatus.setText(ConnectionDefinitions.get_state_description(status))
        color = ConnectionDefinitions.get_state_color(status)
        palette = self.ConnectionScreen.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(*color))
        self.ConnectionScreen.setPalette(palette)

    def set_bitmap(self, bitmap: str = str()):
        self.Bitmap.setText(bitmap)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.hide()
        self.window_close.emit()
        a0.accept()
