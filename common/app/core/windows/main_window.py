from PyQt5.QtWinExtras import QtWin
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QMenu, QPushButton
from common.app.forms.mainwindow import Ui_MainWindow
from common.app.constants.ButtonActions import ButtonAction
from common.app.constants.DataFormats import DataFormats
from common.app.constants.ConnectionStatus import ConnectionStatus
from common.app.core.tools.json_view import JsonView
from common.app.core.tools.action_button import ActionButton
from common.app.core.tools.field_Item import Item
from common.lib.data_models.Transaction import TypeFields, Transaction


class MainWindow(Ui_MainWindow, QMainWindow):
    _window_close: pyqtSignal = pyqtSignal()
    _menu_button_clicked: pyqtSignal = pyqtSignal(QPushButton, str)
    _field_changed: pyqtSignal = pyqtSignal(Item, int)
    _json_view: JsonView

    @property
    def log_browser(self):
        return self.LogArea

    @property
    def window_close(self):
        return self._window_close

    @property
    def button_send(self):
        return self.ButtonSend

    @property
    def button_reset(self):
        return self.ButtonDefault

    @property
    def button_clear_log(self):
        return self.ButtonClearLog

    @property
    def button_settings(self):
        return self.ButtonSettings

    @property
    def button_specification(self):
        return self.ButtonSpecification

    @property
    def button_echo_test(self):
        return self.ButtonEchoTest

    @property
    def button_clear(self):
        return self.ButtonClearMessage

    @property
    def button_copy_log(self):
        return self.ButtonCopyLog

    @property
    def button_copy_bitmap(self):
        return self.ButtonCopyBitmap

    @property
    def button_save(self):
        return self.ButtonSave

    @property
    def button_reconnect(self):
        return self.ButtonReconnect

    @property
    def menu_button_clicked(self):
        return self._menu_button_clicked

    @property
    def button_reverse(self):
        return self.ButtonReverse

    @property
    def button_print(self):
        return self.ButtonPrintData

    @property
    def button_parse_file(self):
        return self.ButtonParseDump

    @property
    def field_changed(self):
        return self._field_changed

    def __init__(self):
        super().__init__()
        self._setup()

    def _setup(self):
        self.setupUi(self)
        self._json_view: JsonView = JsonView()
        self._json_view.itemChanged.connect(self.field_changed.emit)
        self.FieldsTreeLayout.addWidget(self._json_view)
        self.PlusButton = ActionButton("+")
        self.MinusButton = ActionButton("-")
        self.NextLevelButton = ActionButton("↵")

        buttons_layouts_map = {
            self.PlusLayout: self.PlusButton,
            self.MinusLayout: self.MinusButton,
            self.NextLevelLayout: self.NextLevelButton
        }

        for layout, button in buttons_layouts_map.items():
            layout.addWidget(button)

        connection_buttons_map = {
            self.PlusButton: self._json_view.plus,
            self.MinusButton: self._json_view.minus,
            self.NextLevelButton: self._json_view.next_level,
        }

        for button, action in connection_buttons_map.items():
            button.clicked.connect(action)

        buttons_menu_structure = {
            self.ButtonReverse: {
                ButtonAction.LAST: lambda: self.menu_button_clicked.emit(self.ButtonReverse, ButtonAction.LAST),
                ButtonAction.OTHER: lambda: self.menu_button_clicked.emit(self.ButtonReverse, ButtonAction.OTHER),
            },

            self.ButtonPrintData: {
                DataFormats.DUMP: lambda: self.menu_button_clicked.emit(self.ButtonPrintData, DataFormats.DUMP),
                DataFormats.JSON: lambda: self.menu_button_clicked.emit(self.ButtonPrintData, DataFormats.JSON),
                DataFormats.INI: lambda: self.menu_button_clicked.emit(self.ButtonPrintData, DataFormats.INI),
                DataFormats.SPEC: lambda: self.menu_button_clicked.emit(self.ButtonPrintData, DataFormats.SPEC),
                DataFormats.TERM: lambda: self.menu_button_clicked.emit(self.ButtonPrintData, DataFormats.TERM),
            },

            self.ButtonSave: {
                DataFormats.JSON: lambda: self.menu_button_clicked.emit(self.ButtonSave, DataFormats.JSON),
                DataFormats.INI: lambda: self.menu_button_clicked.emit(self.ButtonSave, DataFormats.INI),
                DataFormats.DUMP: lambda: self.menu_button_clicked.emit(self.ButtonSave, DataFormats.DUMP)
            }
        }

        for button, actions in buttons_menu_structure.items():
            button.setMenu(QMenu())

            for action, function in actions.items():
                button.menu().addAction(action, function)
                button.menu().addSeparator()

        QtWin.setCurrentProcessExplicitAppUserModelID("MainWindow.py")

    def clear_log(self):
        self.LogArea.setText(str())

    def get_fields(self) -> TypeFields:
        return self._json_view.generate_fields()

    def get_top_level_field_numbers(self):
        return self._json_view.get_top_level_field_numbers()

    def get_fields_to_generate(self):
        return self._json_view.get_checkboxes()

    def get_mti(self):
        return self.msgtype.currentText()

    def set_log_data(self, data: str = str()):
        self.LogArea.setText(data)

    def get_log_data(self) -> str:
        return self.LogArea.toPlainText()

    def get_bitmap_data(self) -> str:
        return self.Bitmap.text()

    def lock_connection_buttons(self, lock=True):
        for button in (self.ButtonReconnect, self.ButtonSend, self.ButtonEchoTest, self.ButtonReverse):
            button.setDisabled(lock)

    def set_mti_values(self, mti_list: list[str]):
        for mti in mti_list:
            self.msgtype.addItem(mti)

    def set_mti_value(self, mti: str):
        index = self.msgtype.findText(mti, flags=Qt.MatchContains)

        if index == -1:
            raise ValueError(f"Cannot set Message Type Identifier {mti}. Mti not in specification")

        self.msgtype.setCurrentIndex(index)

    def set_fields(self, transaction: Transaction):
        self._json_view.parse_transaction(transaction)
        self.set_bitmap()

    def set_field_value(self, field, field_data):
        self._json_view.set_field_value(field, field_data)

    def clear_message(self):
        self.msgtype.setCurrentIndex(-1)
        self._json_view.clean()

    def set_connection_status(self, status: int):
        self.ConnectionStatus.setText(ConnectionStatus.get_state_description(status))
        color = ConnectionStatus.get_state_color(status)
        palette = self.ConnectionScreen.palette()
        palette.setColor(QPalette.Base, QColor(*color))
        self.ConnectionScreen.setPalette(palette)

    def set_bitmap(self, bitmap: str = str()):
        self.Bitmap.setText(bitmap)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.hide()
        self.window_close.emit()
        a0.accept()
