from os.path import splitext
from logging import debug, info, error, warning
from pydantic import ValidationError
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMenu, QAction
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWinExtras import QtWin
from common.app.forms.mainwindow import Ui_MainWindow
from common.app.core.tools.parser import Parser
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
        debug("Setup MainWindow")
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
        QtWin.setCurrentProcessExplicitAppUserModelID(" ")
        self.setWindowIcon(QIcon(FilePath.MAIN_LOGO))
        self.set_connection_status(QTcpSocket.UnconnectedState, log=False)
        self.set_api_status(state=False)
        self.JsonView: JsonView = JsonView(self.FieldsTree)
        self.JsonView.item_changed.connect(self.set_bitmap)

        button_print_menu = QMenu()
        button_save_menu = QMenu()
        button_reverse_menu = QMenu()

        for action in ("Last", "Other"):
            button_reverse_menu.addAction(action, self.reverse)
            button_reverse_menu.addSeparator()

        for action in DataFormats.get_print_data_formats():
            button_print_menu.addAction(action, self.print_data)
            button_print_menu.addSeparator()

        for action in DataFormats.get_output_file_formats():
            button_save_menu.addAction(action, self.save)
            button_save_menu.addSeparator()

        self.ButtonReverse.setMenu(button_reverse_menu)
        self.ButtonSave.setMenu(button_save_menu)
        self.ButtonPrintData.setMenu(button_print_menu)
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

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.hide()
        self.terminal.disconnect()
        a0.accept()

    def set_api_status(self, state):
        self.terminal.set_api_status(state)

    def run_api(self):
        self.terminal.run_http_server()
        self.set_api_status(state=True)

    def reverse(self, trans_id: str | None = None):
        sender: QAction = self.sender()

        if sender.text().upper() == "OTHER":
            trans_id = self.terminal.get_reversal_id()

            if not trans_id:
                return

            info("Building reversal for transaction %s", trans_id)

        if trans_id is None:
            info("Building reversal for the last transaction")

        self.terminal.reverse(trans_id)

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

        except Exception as E:
            error("Default file parsing error! Exception: %s" % E)

    def lock_connection_buttons(self, lock=True):
        for button in (self.ButtonReconnect, self.ButtonSend, self.ButtonEchoTest):
            button.setDisabled(lock)

    def reconnect(self):
        self.terminal.reconnect()

    def clear_log(self):
        self.LogArea.setText(str())

    def send(self, message: Message = None):
        if message is None:
            try:
                message: Message = self.parser.parse_form(self)
            except Exception as e:
                error(e)
                return

        if message is None:
            return

        try:
            self.terminal.send(message)
        except Exception as e:
            error(e)

    def get_fields(self) -> TypeFields:
        return self.JsonView.generate_fields(validation=True)

    def get_fields_to_generate(self):
        return self.JsonView.get_checkboxes()

    def parse_file(self, filename: str | None = None) -> None:
        if filename is None:
            try:
                filename: str = QFileDialog.getOpenFileName()[0]
            except Exception as get_file_error:
                error("Filename get error: %s", get_file_error)
                return

        if not filename:
            info("No input filename recognized")
            return

        file_name, file_extension = splitext(filename)
        file_extension = file_extension.upper().replace(".", "")

        if file_extension not in DataFormats.get_input_file_formats():
            file_extension = DataFormats.OTHER

        parsing_error_text = "File parsing error: %s"
        message: Message | None = None

        try:
            match file_extension:
                case DataFormats.JSON:
                    message = self.parser.parse_json_file(filename)

                case DataFormats.TXT:
                    message = self.parser.parse_dump_file(filename)

                case DataFormats.INI:
                    message = self.parser.ini_to_message(filename)

                case DataFormats.OTHER:
                    warning("Unknown file extension, trying to guess the format")

                    for data_processor in (self.parser.parse_json_file,
                                           self.parser.parse_dump_file,
                                           self.parser.ini_to_message):
                        try:
                            message = data_processor(filename)

                        except Exception as parsing_error:
                            error("Parsing error: %s", parsing_error)
                            continue

                        else:
                            break
                case _:
                    warning(parsing_error_text, f"Unknown file extension {file_extension}")
                    return

        except ValidationError as validation_error:
            error_text = str(validation_error.json(indent=4))
            error("File validation error: %s", error_text)
            return

        except Exception as parsing_error:
            error(parsing_error_text, parsing_error)
            return

        if not message:
            error("File parsing error")
            return

        self.set_fields(message)
        self.set_mti(message.transaction.message_type_indicator)
        self.set_bitmap()
        info("File successfully parsed: %s", filename)

    def set_mti(self, mti: str):
        index = self.msgtype.findText(f"{mti}: {self.spec.get_desc(mti)}")

        if index == -1:
            error("Cannot set MTI")
            return

        self.msgtype.setCurrentIndex(index)

    def save(self):
        data_format = self.sender().text()

        try:
            filename: str = self.get_output_filename()
            message: Message = self.parser.parse_form(self)

        except Exception as e:
            error(str(e))
            return

        if not filename:
            error("No output filename recognized")
            return

        if message is None:
            error("No data to save")
            return

        try:
            self.terminal.save_message_to_file(filename, message, data_format)
        except Exception as e:
            error(str(e))

    def set_fields(self, message: Message = None):
        self.JsonView.parse_json(message)

    def settings(self):
        self.terminal.settings()

    def specification(self):
        self.terminal.specification()

    def echo_test(self):
        message = self.parser.parse_json_file(FilePath.ECHO_TEST)
        self.send(message)

    def clear_message(self):
        self.msgtype.setCurrentIndex(-1)
        self.JsonView.clean()
        self.set_bitmap()

    def print_data(self):
        data_format = self.sender().text()
        self.terminal.print_data(data_format)

    def set_field_value(self, field, value):
        self.JsonView.set_field_value(field, value)

    @staticmethod
    def get_output_filename():
        filename = QFileDialog()
        filename.setFileMode(QFileDialog.AnyFile)
        filename = filename.getSaveFileName()[0]

        if not filename:
            info("The file did not save, because the operation is canceled")

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

        fields = self.JsonView.generate_fields(validation=False)

        if not fields:
            self.Bitmap.setText(str())
            return

        bitmap: set | str = set(fields.keys())

        for field in self.JsonView.get_checkboxes():
            bitmap.add(field)

        if max(map(int, bitmap)) >= self.spec.MessageLength.first_bitmap_capacity:
            bitmap.add(self.spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY)

        for bit in bitmap:
            if int(bit) not in range(1, self.spec.MessageLength.second_bitmap_capacity + 1):
                bitmap.remove(bit)
                break

        if not bitmap:
            return

        bitmap = ", ".join(sorted(bitmap, key=int))

        self.Bitmap.setText(bitmap)

    def get_mti(self):
        mti = self.msgtype.currentText()

        if len(mti) > 0:
            mti = mti[:self.spec.MessageLength.message_type_length]

        return mti

    def copy_bitmap(self):
        data = self.Bitmap.text()

        if not data:
            error("No data to copy")
            return

        self.terminal.set_clipboard_text(data)

        info("Bitmap copied to clipboard")

    def copy_log(self):
        data = self.LogArea.toPlainText()

        if not data:
            error("No data to copy")
            return

        self.terminal.set_clipboard_text(data)

        info("Log copied to clipboard")
