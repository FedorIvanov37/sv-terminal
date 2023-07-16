from ctypes import windll
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QCloseEvent
from PyQt6.QtWidgets import QMainWindow, QMenu, QPushButton, QApplication, QTreeWidgetItem
from common.gui.forms.mainwindow import Ui_MainWindow
from common.gui.constants.ButtonActions import ButtonAction
from common.gui.constants.DataFormats import DataFormats
from common.gui.constants.ConnectionStatus import ConnectionDefinitions
from common.gui.core.JsonView import JsonView
from common.gui.core.FIeldItem import Item
from common.lib.data_models.Transaction import TypeFields, Transaction
from common.lib.data_models.Config import Config
from PyQt6.QtGui import QKeySequence, QShortcut
from sys import exit


class MainWindow(Ui_MainWindow, QMainWindow):
    _window_close: pyqtSignal = pyqtSignal()
    _menu_button_clicked: pyqtSignal = pyqtSignal(QPushButton, str)
    _field_changed: pyqtSignal = pyqtSignal(Item, int)
    _json_view: JsonView
    _about: pyqtSignal = pyqtSignal()

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
    def button_hotkeys(self):
        return self.ButtonHotkeys

    @property
    def field_changed(self):
        return self._field_changed

    @property
    def about(self):
        return self._about

    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self._setup()

        QShortcut(QKeySequence('Ctrl+Return'), self).activated.connect(self.button_send.clicked.emit)
        QShortcut(QKeySequence('Ctrl+R'), self).activated.connect(self.button_reconnect.clicked.emit)
        QShortcut(QKeySequence('Ctrl+L'), self).activated.connect(self.button_clear_log.clicked.emit)
        QShortcut(QKeySequence('Ctrl+E'), self).activated.connect(self.edit_current_item)
        QShortcut(QKeySequence('Ctrl+Shift+N'), self).activated.connect(self.NextLevelButton.clicked.emit)
        QShortcut(QKeySequence('Ctrl+Q'), self).activated.connect(exit)
        QShortcut(QKeySequence(QKeySequence.StandardKey.New), self).activated.connect(self.PlusButton.clicked.emit)
        QShortcut(QKeySequence(QKeySequence.StandardKey.Delete), self).activated.connect(self.MinusButton.clicked.emit)
        QShortcut(QKeySequence(QKeySequence.StandardKey.HelpContents), self).activated.connect(self.about.emit)
        QShortcut(QKeySequence(QKeySequence.StandardKey.Save), self).activated.connect(self.button_save.showMenu)
        QShortcut(QKeySequence(QKeySequence.StandardKey.Print), self).activated.connect(self.button_print.showMenu)
        QShortcut(QKeySequence(QKeySequence.StandardKey.Open), self).activated.connect(
            self.button_parse_file.clicked.emit
        )
        QShortcut(QKeySequence('Ctrl+T'), self).activated.connect(
            lambda: self.menu_button_clicked.emit(self.button_print, DataFormats.TERM)
        )
        QShortcut(QKeySequence('Ctrl+Shift+Return'), self).activated.connect(
            lambda: self.menu_button_clicked.emit(self.button_reverse, ButtonAction.LAST)
        )

    def edit_current_item(self):
        if not self._json_view.hasFocus():
            self._json_view.setFocus()

        if not (item := self._json_view.currentItem()):
            return

        self._json_view.edit_item(item, 1)

    def _setup(self):
        self.setupUi(self)
        self._json_view: JsonView = JsonView(self.config)
        self._json_view.itemChanged.connect(self.field_changed.emit)
        self.FieldsTreeLayout.addWidget(self._json_view)
        self.PlusButton = QPushButton("✚")
        self.MinusButton = QPushButton("━")
        self.NextLevelButton = QPushButton("🡾")

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

        #
        # Why it does not work?
        #
        # button_actions_map = {
        #     self.ButtonSave: DataFormats.get_output_file_formats(),
        #     self.ButtonReverse: ButtonAction.get_reversal_actions(),
        #     self.ButtonPrintData: DataFormats.get_print_data_formats(),
        # }
        #
        # for button, formats in button_actions_map.items():
        #     button.setMenu(QMenu())
        #
        #     for action in formats:
        #         button.menu().addAction(action, lambda: self.menu_button_clicked.emit(button, action))
        #         button.menu().addSeparator()
        #

        buttons_menu_structure = {  # And why it works instead?
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
                DataFormats.DUMP: lambda: self.menu_button_clicked.emit(self.ButtonSave, DataFormats.DUMP),
            }
        }

        for button, actions in buttons_menu_structure.items():
            button.setMenu(QMenu())

            for action, function in actions.items():
                button.menu().addAction(action, function)
                button.menu().addSeparator()

        windll.shell32.SetCurrentProcessExplicitAppUserModelID("MainWindow.py")

    def clear_log(self):
        self.LogArea.setText(str())

    def get_fields(self) -> TypeFields:
        return self._json_view.generate_fields()

    def get_top_level_field_numbers(self):
        return self._json_view.get_top_level_field_numbers()

    def get_fields_to_generate(self):
        return self._json_view.get_checkboxes()

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
        return self._json_view.get_field_data(field_number)

    def set_mti_value(self, mti: str):
        index = self.msgtype.findText(mti, flags=Qt.MatchFlag.MatchContains)

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
