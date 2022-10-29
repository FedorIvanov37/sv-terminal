from json import dumps
from logging import error, info
from pydantic import ValidationError
from PyQt5 import QtWidgets
from PyQt5.Qt import QApplication
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
from common.app.core.windows.main_window import MainWindow
from common.app.core.windows.reversal_window import ReversalWindow
from common.app.core.windows.settings_window import SettingsWindow
from common.app.core.windows.spec_window import SpecWindow
from common.app.core.tools.parser import Parser
from common.app.core.tools.logger import Logger
from common.app.core.tools.transaction_queue import TransactionQueue
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.core.tools.fields_generator import FieldsGenerator
from common.app.core.tools.validator import Validator
from common.app.constants.TextConstants import TextConstants
from common.app.constants.DataFormats import DataFormats
from common.app.constants.FilePath import FilePath
from common.app.data_models.config import Config
from common.app.data_models.transaction import Transaction
from common.app.constants.ButtonActions import ButtonAction
from common.app.core.tools.connector import ConnectionWorker


class SvTerminal(QObject):
    _config: Config = Config.parse_file(FilePath.CONFIG)
    _pyqt_application = QtWidgets.QApplication([])
    _validator = Validator(_config)
    _spec: EpaySpecification = EpaySpecification()
    _need_reconnect: pyqtSignal = pyqtSignal()

    @property
    def config(self):
        return self._config

    @property
    def validator(self):
        return self._validator

    @property
    def spec(self):
        return self._spec

    def __init__(self):
        super(SvTerminal, self).__init__()
        self.parser: Parser = Parser(self.config)
        self.generator = FieldsGenerator(self.config)
        self.window: MainWindow = MainWindow()
        self.logger: Logger = Logger(self.window.log_browser, self.config)
        self.connector: ConnectionWorker = ConnectionWorker(self.config)
        self.trans_queue: TransactionQueue = TransactionQueue(self.config, self.connector)
        self.connector.socker_error.connect(self.socket_error)
        self.setup()

    def run(self):
        status = self._pyqt_application.exec_()
        exit(status)

    def setup(self):
        self.connect_widgets()
        self.window.set_mti_values(self.spec.get_mti_list())
        self.window.set_log_data(TextConstants.HELLO_MESSAGE)
        self.window.setWindowIcon(QIcon(FilePath.MAIN_LOGO))
        self.window.set_connection_status(QTcpSocket.UnconnectedState)

        if self.config.terminal.connect_on_startup:
            self.reconnect()

        if self.config.terminal.process_default_dump:
            self.set_default_values()

        self.window.show()

    def connect_widgets(self):
        window = self.window

        buttons_connection_map = {
            window.button_clear_log: self.window.clear_log,
            window.button_send: self.send,
            window.button_reset: self.set_default_values,
            window.button_settings: self.settings,
            window.button_specification: self.specification,
            window.button_echo_test: self.echo_test,
            window.button_clear: self.clear_message,
            window.button_copy_log: self.copy_log,
            window.button_copy_bitmap: self.copy_bitmap,
            window.button_reconnect: self.reconnect,
            window.button_parse_file: self.parse_file
        }

        for button, slot in buttons_connection_map.items():
            button.clicked.connect(slot)

        window.window_close.connect(self.disconnect)
        window.menu_button_clicked.connect(self.proces_button_menu)
        window.field_changed.connect(self.set_bitmap)
        self.trans_queue.incoming_transaction.connect(self.logger.print_dump)
        self.trans_queue.incoming_transaction.connect(self.logger.print_transaction)
        self.connector.connected.connect(self.connected)
        self.connector.disconnected.connect(self.disconnected)
        self.connector.connection_started.connect(self.window.lock_connection_buttons)
        self.connector.connection_finished.connect(lambda: self.window.lock_connection_buttons(lock=False))
        self._need_reconnect.connect(self.connector.connect_sv)
        self.trans_queue.transaction_matched.connect(self.transaction_matched)

    def socket_error(self):
        if self.connector.error() == -1:  # TODO
            return

        error("SVFE host received a socket error: %s", self.connector.error_string())

    def connected(self):
        self.window.set_connection_status(QTcpSocket.ConnectedState)
        info("SVFE host connection ESTABLISHED")

    def disconnected(self):
        self.window.set_connection_status(QTcpSocket.UnconnectedState)
        info("SVFE host DISCONNECTED")

    def send(self, request: Transaction | None = None):
        if self.config.debug.clear_log:
            self.window.clear_log()

        if not request:
            try:
                request: Transaction = self.parser.parse_form(self.window)
            except Exception as building_error:
                error(f"Transaction building error")
                [error(err.strip()) for err in str(building_error).splitlines()]
                return

        info(f"Processing transaction ID [{request.trans_id}]")

        if request.generate_fields:
            request: Transaction = self.generator.set_generated_fields(request)

        if self.config.fields.send_internal_id:
            request: Transaction = self.generator.set_trans_id_to_47_072(request)

        if self.sender() is self.window.button_send:
            self.set_generated_fields(request)

        if self.config.fields.validation:
            try:
                self.validator.validate_transaction(request)
            except (ValueError, TypeError) as validation_error:
                error(f"Transaction validation error {validation_error}")
                return

        self.logger.print_dump(request)
        self.logger.print_transaction(request)
        self.trans_queue.put_transaction(request)

    def settings(self):
        SettingsWindow(self.config).exec_()

    def specification(self):
        spec_window: SpecWindow = SpecWindow(self.window)
        spec_window.spec_accepted.connect(lambda: info("Specification accepted"))
        spec_window.exec_()

    @staticmethod
    def get_output_filename():
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        filename = file_dialog.getSaveFileName()[0]
        return filename

    def save_transaction_to_file(self, file_format: str) -> None:
        if not (filename := self.get_output_filename()):
            error("No output filename recognized")
            return

        try:
            transaction = self.parser.parse_form(self.window)
        except Exception as file_saving_error:
            error("File saving error: %s", file_saving_error)
            return

        data_processing_map = {
            DataFormats.JSON: lambda _trans: dumps(_trans.dict(), indent=4),
            DataFormats.INI: lambda _trans: self.parser.transaction_to_ini_string(_trans),
            DataFormats.DUMP: lambda _trans: self.parser.create_sv_dump(_trans)[1:]
        }

        if not (data_processing_function := data_processing_map.get(file_format)):
            error("Unknown output file format")
            return

        if not (file_data := data_processing_function(transaction)):
            error("No data to save")
            return

        with open(filename, "w") as file:
            file.write(file_data)

        info(f"The transaction was saved successfully to {filename}")

    @staticmethod
    def transaction_matched(tranaction: Transaction, resp_time_seconds: float):
        info(f"Transaction ID [{tranaction.trans_id}] matched. Response time seconds: {resp_time_seconds}")

    def disconnect(self):
        self.connector.disconnect_sv()

    def reconnect(self):
        info("[Re]connecting...")
        self._need_reconnect.emit()

    def print_data(self, data_format: str) -> None:
        if data_format not in DataFormats.get_print_data_formats():
            error("Wrong format of output data: %s", data_format)
            return

        data_processing_map = {
            DataFormats.JSON: lambda: dumps(self.parser.parse_form(self.window).dict(), indent=4),
            DataFormats.DUMP: lambda: self.parser.create_sv_dump(self.parser.parse_form(self.window)),
            DataFormats.INI: lambda: self.parser.transaction_to_ini_string(self.parser.parse_form(self.window)),
            DataFormats.TERM: lambda: TextConstants.HELLO_MESSAGE,
            DataFormats.SPEC: lambda: dumps(self.spec.spec.dict(), indent=4)
        }

        if not (function := data_processing_map.get(data_format)):
            error(f"Wrong data format for printing: {data_format}")
            return

        try:
            self.window.set_log_data(function())
        except (ValidationError, ValueError) as validation_error:
            error(f"{validation_error}")

    def copy_log(self):
        self.set_clipboard_text(self.window.get_log_data())

    def copy_bitmap(self):
        self.set_clipboard_text(self.window.get_bitmap_data())

    @staticmethod
    def set_clipboard_text(data: str = str()) -> None:
        QApplication.clipboard().setText(data)

    def show_reversal_window(self):
        reversible_transactions_list: list[Transaction] = self.trans_queue.get_reversible_transactions()
        reversal_window = ReversalWindow(reversible_transactions_list)

        if reversal_window.exec_():
            return reversal_window.reversal_id

        info("Reversal sending is cancelled by user")

    def reverse_transaction(self, last_or_other: str):
        match last_or_other:
            case ButtonAction.LAST:
                if not (original_id := self.trans_queue.get_last_reversible_transaction_id()):
                    error("Transaction Queue has no reversible transactions")
                    return

            case ButtonAction.OTHER:
                if not (original_id := self.show_reversal_window()):
                    error("No transaction ID recognized. The Reversal wasn't sent")
                    return

            case _:
                error("Wrong action during reverse the transaction")
                return

        original: Transaction = self.trans_queue.get_transaction(original_id)
        reversal: Transaction = self.build_reversal(original)

        if not reversal:
            return

        self.send(reversal)

    def build_reversal(self, original_transaction: Transaction) -> Transaction | None:
        if not (original_transaction.matched and original_transaction.match_id):
            error(f"Lost response for transaction {original_transaction.trans_id}. Cannot build the reversal")
            return

        reversal_trans_id = original_transaction.trans_id + "_R"
        existed_reversal = self.trans_queue.get_transaction(reversal_trans_id)

        if existed_reversal:
            self.trans_queue.remove_from_queue(existed_reversal)
            transaction: Transaction = Transaction.parse_obj(existed_reversal)
            return transaction

        fields = original_transaction.data_fields.copy()

        for field in self.spec.get_reversal_fields():
            fields[field] = original_transaction.data_fields.get(field)

        if self.config.fields.build_fld_90:
            fields[self.spec.FIELD_SET.FIELD_090_ORIGINAL_DATA_ELEMENTS] = \
                self.generator.generate_original_data_elements(original_transaction)

        reversal_mti = self.spec.get_reversal_mti(original_transaction.message_type)

        reversal = Transaction(
            message_type=reversal_mti,
            data_fields=fields,
            trans_id=reversal_trans_id,
            generate_fields=list(),
        )

        return reversal

    def set_default_values(self):
        try:
            self.parse_file(FilePath.DEFAULT_FILE)
            info("Default file parsed")

        except Exception as parsing_error:
            error("Default file parsing error! Exception: %s" % parsing_error)

    def parse_file(self, filename: str | None = None) -> None:
        if not filename and not (filename := QFileDialog.getOpenFileName()[0]):
            info("No input filename recognized")
            return

        try:
            transaction: Transaction = self.parser.parse_file(filename)
        except (TypeError, ValueError, Exception) as parsing_error:
            error(f"File parsing error: {parsing_error}")
            return

        self.window.set_mti_value(transaction.message_type)
        self.window.set_fields(transaction)
        self.set_bitmap()

        if self.sender() is self.window.button_parse_file:
            info(f"File parsed: {filename}")

    def set_generated_fields(self, transaction: Transaction):
        for field in transaction.generate_fields:
            if not (field_data := transaction.data_fields.get(field)):
                error("Lost field data for field %s")

            if not self.spec.can_be_generated([field]):
                error(f"Field {field} cannot be generated")
                return

            self.window.set_field_value(field, field_data)

    def echo_test(self):
        transaction: Transaction = self.parser.parse_file(FilePath.ECHO_TEST)
        self.send(transaction)

    def clear_message(self):
        self.window.clear_message()
        self.set_bitmap()

    def set_bitmap(self):
        bitmap: set[str] = set()

        for bit in self.window.get_top_level_field_numbers():
            if not bit.isdigit():
                continue

            if int(bit) not in range(1, self.spec.MessageLength.second_bitmap_capacity + 1):
                continue

            if int(bit) >= self.spec.MessageLength.first_bitmap_capacity:
                bitmap.add(self.spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY)

            bitmap.add(bit)

        self.window.set_bitmap(", ".join(sorted(bitmap, key=int)))

    def proces_button_menu(self, button, action: str):
        data_processing_map = {
            self.window.button_save: lambda _action: self.save_transaction_to_file(_action),
            self.window.button_reverse: lambda _action: self.reverse_transaction(_action),
            self.window.button_print: lambda _action: self.print_data(_action)
        }

        if not (function := data_processing_map.get(button)):
            return

        function(action)
