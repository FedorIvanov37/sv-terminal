from logging import info, error
from PyQt5.QtGui import QPalette, QColor, QIcon, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWinExtras import QtWin
from common.app.forms.mainwindow import Ui_MainWindow
from common.app.core.tools.parser import Parser
from common.app.constants.ButtonActions import ButtonAction
from common.app.constants.ConnectionStatus import ConnectionStatus
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.constants.FilePath import FilePath
from common.app.constants.TextConstants import TextConstants
from common.app.constants.DataFormats import DataFormats
from common.app.core.tools.json_view import JsonView
from common.app.data_models.message import TypeFields
from common.app.data_models.config import Config
from common.app.core.tools.action_button import ActionButton
from common.app.data_models.transaction import Transaction


class MainWindow(Ui_MainWindow, QMainWindow):
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    @property
    def log_browser(self):
        return self.LogArea

    @property
    def button_send(self):
        return self.ButtonSend

    def __init__(self, config: Config, terminal):
        super().__init__()
        self.config: Config = config
        self.terminal = terminal
        self.parser: Parser = Parser(self.config)
        self._setup()

    def _connect_buttons(self):
        buttons_connection_scheme = {  # Define method of MainWindow for each button object
            self.ButtonSend: self.send,
            self.ButtonClearLog: self.clear_log,
            self.ButtonParseDump: self.parse_file,
            self.ButtonClearMessage: self.clear_message,
            self.ButtonDefault: self.set_default_values,
            self.ButtonEchoTest: self.echo_test,
            self.ButtonReconnect: self.reconnect,
            self.ButtonSpecification: self.specification,
            self.ButtonSettings: self.settings,
            self.ButtonCopyLog: self.copy_log,
            self.ButtonCopyBitmap: self.copy_bitmap,
            self.PlusButton: self.plus,
            self.MinusButton: self.minus,
            self.NextLevelButton: self.next_level,
        }

        for button, method in buttons_connection_scheme.items():
            button.pressed.connect(method)

    def _setup(self):
        self.setupUi(self)
        self.setWindowIcon(QIcon(FilePath.MAIN_LOGO))
        self.set_connection_status(QTcpSocket.UnconnectedState, log=False)
        self.json_view: JsonView = JsonView(self.config, self.FieldsTree)
        self.json_view.tree.itemChanged.connect(self.set_bitmap)
        self.PlusButton = ActionButton("+")
        self.MinusButton = ActionButton("-")
        self.NextLevelButton = ActionButton("↵")

        layout_buttons_map = {
            self.PlusLayout: self.PlusButton,
            self.MinusLayout: self.MinusButton,
            self.NextLevelLayout: self.NextLevelButton
        }

        buttons_menu_structure = {
            self.ButtonReverse: {
                ButtonAction.LAST: lambda: self.reverse(reverse_last_transaction=True),
                ButtonAction.OTHER: lambda: self.reverse(reverse_last_transaction=False)
            },

            self.ButtonPrintData: {
                DataFormats.DUMP: lambda: self.print_data(DataFormats.DUMP),
                DataFormats.JSON: lambda: self.print_data(DataFormats.JSON),
                DataFormats.INI: lambda: self.print_data(DataFormats.INI),
                DataFormats.SPEC: lambda: self.print_data(DataFormats.SPEC),
                DataFormats.SV_TERMINAL: lambda: self.print_data(DataFormats.SV_TERMINAL)
            },

            self.ButtonSave: {
                DataFormats.JSON: lambda: self.save(DataFormats.JSON),
                DataFormats.INI: lambda: self.save(DataFormats.INI),
                DataFormats.DUMP: lambda: self.save(DataFormats.DUMP)
            }
        }

        for layout, button in layout_buttons_map.items():
            layout.addWidget(button)

        for button, actions in buttons_menu_structure.items():
            button.setMenu(QMenu())

            for action, function in actions.items():
                button.menu().addAction(action, function)
                button.menu().addSeparator()

        for mti in self.spec.get_mti_list():
            self.msgtype.addItem(mti)

        if self.config.terminal.process_default_dump:
            self.set_default_values()

        self.set_bitmap()
        self.LogArea.setText(TextConstants.HELLO_MESSAGE)
        self._connect_buttons()
        QtWin.setCurrentProcessExplicitAppUserModelID("MainWindow.py")

    def plus(self):
        self.json_view.plus()

    def minus(self):
        self.json_view.minus()

    def next_level(self):
        self.json_view.next_level()

    def reconnect(self):
        self.terminal.reconnect()

    def clear_log(self):
        self.LogArea.setText(str())

    def get_fields(self) -> TypeFields:
        return self.json_view.generate_fields()

    def get_fields_to_generate(self):
        return self.json_view.get_checkboxes()

    def get_mti(self):
        mti: str = self.msgtype.currentText()
        mti: str = mti[:self.spec.MessageLength.message_type_length]
        return mti

    def copy_bitmap(self):
        self.terminal.set_clipboard_text(self.Bitmap.text())
        info("Bitmap copied to clipboard")

    def copy_log(self):
        self.terminal.set_clipboard_text(self.LogArea.toPlainText())
        info("Log copied to clipboard")

    def set_default_values(self):
        try:
            self.parse_file(FilePath.DEFAULT_FILE)
            info("Default file parsed")

        except Exception as parsing_error:
            error("Default file parsing error! Exception: %s" % parsing_error)

    def lock_connection_buttons(self, lock=True):
        for button in (self.ButtonReconnect, self.ButtonSend, self.ButtonEchoTest, self.ButtonReverse):
            button.setDisabled(lock)

    def send(self) -> None:
        try:
            transaction: Transaction = self.parser.parse_form(self)
        except Exception as building_error:
            error(f"Transaction building error")
            [error(err.strip()) for err in str(building_error).splitlines()]
            return

        try:
            self.terminal.send(transaction)
        except Exception as sending_error:
            error(f"Transaction sending error: {sending_error}")

    def reverse(self, reverse_last_transaction: bool):
        original_transaction_id: str | None = None

        if reverse_last_transaction:
            original_transaction_id = self.terminal.get_last_reversible_transaction_id()

        if not reverse_last_transaction:
            original_transaction_id = self.terminal.show_reversal_window()

        if not original_transaction_id:
            return

        self.terminal.reverse_transaction(original_transaction_id)

    def parse_file(self, filename: str | None = None) -> None:
        if filename is None and not (filename := QFileDialog.getOpenFileName()[0]):
            info("No input filename recognized")
            return

        try:
            transaction: Transaction = self.parser.parse_file(filename)
        except (TypeError, ValueError, Exception) as parsing_error:
            error(f"File parsing error: {parsing_error}")
            return

        self.set_mti(transaction.message_type)
        self.set_fields(transaction)

        if self.sender() is self.ButtonParseDump:
            info(f"File parsed: {filename}")

    def set_mti(self, mti: str):
        index = self.msgtype.findText(mti, flags=Qt.MatchContains)

        if index == -1:
            error(f"Cannot set Message Type Identifier {mti}. Mti not in specification")
            return

        self.msgtype.setCurrentIndex(index)

    def save(self, data_format) -> None:
        try:
            if not (filename := self.get_output_filename()):
                error("No output filename recognized")
                return

            if not (transaction := self.parser.parse_form(self)):
                error("No data to save")
                return

            self.terminal.save_transaction_to_file(transaction, filename, data_format)

        except Exception as file_saving_error:
            error("File saving error: %s", file_saving_error)

    def set_generated_fields(self, transaction: Transaction):
        for field in transaction.generate_fields:

            if not (field_data := transaction.data_fields.get(field)):
                error("Lost field data for field %s")

            self.json_view.set_field_value(field, field_data)

    def set_fields(self, transaction: Transaction):
        self.json_view.parse_transaction(transaction)
        self.set_bitmap()

    def settings(self):
        self.terminal.settings()

    def specification(self):
        self.terminal.specification()

    def echo_test(self):
        transaction: Transaction = self.parser.parse_file(FilePath.ECHO_TEST)
        self.terminal.send(transaction)

    def clear_message(self):
        self.msgtype.setCurrentIndex(-1)
        self.json_view.clean()
        self.set_bitmap()

    def print_data(self, data_format):
        if data_format not in DataFormats.get_print_data_formats():
            error("Wrong data format for printing!")
            return

        try:
            self.terminal.print_data(data_format)
        except Exception as printing_error:
            error(f"Error: {printing_error}")

    def set_field_value(self, field, value):
        self.json_view.set_field_value(field, value)

    @staticmethod
    def get_output_filename():
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        filename = file_dialog.getSaveFileName()[0]
        return filename

    def set_connection_status(self, status: int, log=True):
        if log:
            info("Connection status changed to %s", ConnectionStatus.get_state_description(status))

        self.ConnectionStatus.setText(ConnectionStatus.get_state_description(status))
        color = ConnectionStatus.get_state_color(status)
        palette = self.ConnectionScreen.palette()
        palette.setColor(QPalette.Base, QColor(*color))
        self.ConnectionScreen.setPalette(palette)

    def set_bitmap(self):
        if not (fields_set := self.json_view.get_field_set()):
            return

        bitmap: set[str] = set(fields_set)

        for bit in bitmap.copy():
            if not bit.isdigit():
                return

            if int(bit) not in range(1, self.spec.MessageLength.second_bitmap_capacity + 1):
                return

        if not bitmap:
            return

        if max(map(int, bitmap)) >= self.spec.MessageLength.first_bitmap_capacity:
            bitmap.add(self.spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY)

        bitmap: str = ", ".join(sorted(bitmap, key=int))

        self.Bitmap.setText(bitmap)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.hide()
        self.terminal.disconnect()
        a0.accept()
