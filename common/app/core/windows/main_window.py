from common.app.core.windows.reversal_window import ReversalWindow
from logging import info, error
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMenu
from PyQt5.QtGui import QCloseEvent
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
from common.app.data_models.message import Message
from common.app.data_models.config import Config
from common.app.core.tools.action_button import ActionButton


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
        self.setupUi(self)
        self.parser: Parser = Parser(self.config)
        self.setup()

    def setup(self):
        self._setup()

    def _connect(self):
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
            self.ButtonRunApi: self.run_api
        }

        for button, method in buttons_connection_scheme.items():
            button.pressed.connect(method)

    def _setup(self):
        QtWin.setCurrentProcessExplicitAppUserModelID("MainWindow.py")
        self.setWindowIcon(QIcon(FilePath.MAIN_LOGO))
        self.set_connection_status(QTcpSocket.UnconnectedState, log=False)
        self.set_api_status(state=False)
        self.JsonView: JsonView = JsonView(self.FieldsTree)
        self.JsonView.item_changed.connect(self.set_bitmap)

        for button in (self.ButtonReverse, self.ButtonSave, self.ButtonPrintData):
            button.setMenu(QMenu())

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

        for button, actions in buttons_menu_structure.items():
            button.setMenu(QMenu())

            for action, function in actions.items():
                button.menu().addAction(action, function)
                button.menu().addSeparator()

        self.PlusButton = ActionButton("+")
        self.MinusButton = ActionButton("-")
        self.NextLevelButton = ActionButton("↵")
        self.PlusLayout.addWidget(self.PlusButton)
        self.MinusLayout.addWidget(self.MinusButton)
        self.NextLevelLayout.addWidget(self.NextLevelButton)

        for mti in self.spec.get_mti_list():
            self.msgtype.addItem(mti)

        if self.config.terminal.process_default_dump:
            self.set_default_values()

        self.set_bitmap()
        self.LogArea.setText(TextConstants.HELLO_MESSAGE)
        self._connect()

    def set_api_status(self, state):
        self.terminal.set_api_status(state)

    def run_api(self):
        self.terminal.run_http_server()
        self.set_api_status(state=True)

    def get_last_transaction_id(self):
        transaction_id = str()

        for transaction in self.terminal.get_reversible_transactions():
            if transaction.trans_id > transaction_id:
                transaction_id = transaction.trans_id

        if not transaction_id:
            error("Transaction Queue has no reversible transactions")

        return transaction_id

    def show_reversal_window(self):
        transaction_list: list = self.terminal.get_reversible_transactions()
        reversal_window = ReversalWindow(transaction_list)

        if reversal_window.exec_():
            if not reversal_window.reversal_id:
                error("No transaction ID recognized. The Reversal wasn't sent")

            return reversal_window.reversal_id

        info("Reversal sending is cancelled by user")

    def reverse(self, reverse_last_transaction: bool):
        if reverse_last_transaction:
            original_transaction_id = self.get_last_transaction_id()

        else:
            original_transaction_id = self.show_reversal_window()

        if original_transaction_id:
            self.terminal.reverse_transaction(original_transaction_id)

    def plus(self):
        self.JsonView.plus()

    def minus(self):
        self.JsonView.minus()

    def next_level(self):
        self.JsonView.next_level()

    def set_default_values(self):
        try:
            self.parse_file(FilePath.DEFAULT_FILE)
            info("Default file parsed")

        except Exception as parsing_error:
            error("Default file parsing error! Exception: %s" % parsing_error)

    def lock_connection_buttons(self, lock=True):
        for button in (self.ButtonReconnect, self.ButtonSend, self.ButtonEchoTest, self.ButtonReverse):
            button.setDisabled(lock)

    def reconnect(self):
        self.terminal.reconnect()

    def clear_log(self):
        self.LogArea.setText(str())

    def send(self) -> None:
        try:
            message: Message = self.parser.parse_form(self)
            self.terminal.send(message)
        except Exception as sending_error:
            error(f"Message sending error: {sending_error}")

    def get_fields(self) -> TypeFields:
        return self.JsonView.generate_fields(validation=True)

    def get_fields_to_generate(self):
        return self.JsonView.get_checkboxes()

    def parse_file(self, filename: str | None = None) -> None:
        if filename is None and not (filename := QFileDialog.getOpenFileName()[0]):
            info("No input filename recognized")
            return

        try:
            message = self.parser.parse_file(filename)
        except (TypeError, ValueError, Exception) as parsing_error:
            error(f"File parsing error: {parsing_error}")
            return

        self.set_mti(message.transaction.message_type)
        self.set_fields(message)

        info("File successfully parsed: %s", filename)

    def set_mti(self, mti: str):
        index = self.msgtype.findText(f"{mti}: {self.spec.get_desc(mti)}")

        if index == -1:
            error("Cannot set MTI")
            return

        self.msgtype.setCurrentIndex(index)

    def save(self, data_format) -> None:
        try:
            if not (filename := self.get_output_filename()):
                error("No output filename recognized")
                return

            if not (message := self.parser.parse_form(self)):
                error("No data to save")
                return

            self.terminal.save_message_to_file(message, filename, data_format)

        except Exception as file_saving_error:
            error("File saving error: %s", file_saving_error)

    def set_fields(self, message: Message):
        self.JsonView.parse_message(message)
        self.set_bitmap()

    def set_generated_fields(self, message: Message):
        for field in message.config.generate_fields:

            if (field_data := message.transaction.fields.get(field, str())) is str():
                error("Lost field data for field %s")

            self.JsonView.set_field_value(field, field_data)

    def settings(self):
        self.terminal.settings()

    def specification(self):
        self.terminal.specification()

    def echo_test(self):
        message = self.parser.parse_file(FilePath.ECHO_TEST)
        self.terminal.send(message)

    def clear_message(self):
        self.msgtype.setCurrentIndex(-1)
        self.JsonView.clean()
        self.set_bitmap()

    def print_data(self, data_format):
        if data_format not in DataFormats.get_print_data_formats():
            error("Wrong data format for printing!")
            return

        self.terminal.print_data(data_format)

    def set_field_value(self, field, value):
        self.JsonView.set_field_value(field, value)

    @staticmethod
    def get_output_filename():
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        filename = file_dialog.getSaveFileName()[0]
        return filename

    def set_api_status(self, state):
        self.ApiStatus.setText("API Running" if state else "API shutdown")
        color = ConnectionStatus.GREEN if state else ConnectionStatus.RED
        palette = self.ApiScreen.palette()
        palette.setColor(QPalette.Base, QColor(*color))
        self.ApiScreen.setPalette(palette)

    def set_connection_status(self, status: int, log=True):
        if log:
            info("Connection status changed to %s", ConnectionStatus.get_state_description(status))

        self.ConnectionStatus.setText(ConnectionStatus.get_state_description(status))
        color = ConnectionStatus.get_state_color(status)
        palette = self.ConnectionScreen.palette()
        palette.setColor(QPalette.Base, QColor(*color))
        self.ConnectionScreen.setPalette(palette)

    def set_bitmap(self):
        default_bitmap_text = str()

        if not (fields := self.JsonView.generate_fields(validation=False)):
            self.Bitmap.setText(default_bitmap_text)
            return

        bitmap: set = set(fields)

        for bit in bitmap.copy():
            if int(bit) not in range(1, self.spec.MessageLength.second_bitmap_capacity + 1):
                bitmap.remove(bit)

        if not bitmap:
            self.Bitmap.setText(default_bitmap_text)
            return

        if max(map(int, bitmap)) >= self.spec.MessageLength.first_bitmap_capacity:
            bitmap.add(self.spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY)

        bitmap: str = ", ".join(sorted(bitmap, key=int))

        self.Bitmap.setText(bitmap)

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

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.hide()
        self.terminal.disconnect()
        a0.accept()
