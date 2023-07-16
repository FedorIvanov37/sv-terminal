from json import dumps
from logging import error, info, warning
from pydantic import ValidationError
from PyQt6.QtWidgets import QApplication
from PyQt6.QtNetwork import QTcpSocket
from PyQt6.QtWidgets import QFileDialog
from common.lib.core.Logger import LogStream, getLogger, Formatter
from common.gui.windows.main_window import MainWindow
from common.gui.windows.reversal_window import ReversalWindow
from common.gui.windows.settings_window import SettingsWindow
from common.gui.windows.spec_window import SpecWindow
from common.gui.windows.hotkeys_hint_window import HotKeysHintWindow
from common.gui.windows.about_window import AboutWindow
from common.gui.constants.TextConstants import TextConstants
from common.gui.constants.DataFormats import DataFormats
from common.gui.constants.TermFilesPath import TermFilesPath
from common.gui.constants.ButtonActions import ButtonAction
from common.lib.constants.LogDefinition import LogDefinition
from common.gui.core.WirelessHandler import WirelessHandler
from common.gui.core.ConnectionThread import ConnectionThread
from common.lib.core.LogPrinter import LogPrinter
from common.lib.data_models.Config import Config
from common.lib.data_models.Transaction import Transaction, TypeFields
from common.lib.core.Terminal import SvTerminal


class SvTerminalGui(SvTerminal):
    connector: ConnectionThread

    def __init__(self, config: Config):
        super(SvTerminalGui, self).__init__(config, ConnectionThread(config))
        self.window: MainWindow = MainWindow(self.config)
        self.log_printer = LogPrinter()
        self.setup()

    def setup(self):
        self.create_window_logger()
        self.log_printer.print_startup_info(self.config)
        self.connect_widgets()
        self.window.set_mti_values(self.spec.get_mti_list())
        self.window.set_connection_status(QTcpSocket.SocketState.UnconnectedState)
        self.print_data(DataFormats.TERM)

        if self.config.terminal.process_default_dump:
            self.set_default_values()

        self.window.show()

    def connect_widgets(self):
        window = self.window

        terminal_connections_map = {
            window.clear_log: window.clean_window_log,
            window.send: self.send,
            window.reset: self.set_default_values,
            window.echo_test: self.echo_test,
            window.clear: self.clear_message,
            window.copy_log: self.copy_log,
            window.copy_bitmap: self.copy_bitmap,
            window.reconnect: self.reconnect,
            window.parse_file: self.parse_file,
            window.settings: lambda: self.run_child_window(SettingsWindow, self.config),
            window.hotkeys: lambda: self.run_child_window(HotKeysHintWindow),
            window.specification: lambda: self.run_child_window(SpecWindow),
            window.about: lambda: self.run_child_window(AboutWindow),
            window.window_close: self.stop_sv_terminal,
            window.reverse: self.perform_reversal,
            window.print: self.print_data,
            window.save: self.save_transaction_to_file,
            window.field_changed: self.set_bitmap,
            window.field_removed: self.set_bitmap,
            window.field_added: self.set_bitmap,
            self.connector.stateChanged: self.set_connection_status,
        }

        for signal, slot in terminal_connections_map.items():
            signal.connect(slot)

    @staticmethod
    def run_child_window(child_window, *args, **kwargs):
        child_window(*args, **kwargs).exec()

    def stop_sv_terminal(self):
        self.connector.stop_thread()

    def reconnect(self):
        SvTerminal.reconnect(self)

    def set_connection_status(self):
        self.window.set_connection_status(self.connector.state())

        if self.connector.state() is QTcpSocket.SocketState.ConnectingState:
            self.window.block_connection_buttons()
            return

        self.window.unblock_connection_buttons()

    def create_window_logger(self):
        formatter = Formatter(LogDefinition.FORMAT, LogDefinition.DISPLAY_DATE_FORMAT, LogDefinition.MARK_STYLE)
        wireless_handler = WirelessHandler()
        stream = LogStream(self.window.log_browser)
        wireless_handler.new_record_appeared.connect(lambda record: stream.write(data=record))
        wireless_handler.setFormatter(formatter)
        logger = getLogger()
        logger.addHandler(wireless_handler)

    def perform_reversal(self, id_source: str):
        lost_transaction_message = "Cannot reverse transaction, lost transaction ID or non-reversible MTI"

        match id_source:
            case ButtonAction.LAST:
                transaction_id = self.trans_queue.get_last_reversible_transaction_id()

            case ButtonAction.OTHER:
                transaction_id = self.show_reversal_window()

            case _:
                error(lost_transaction_message)
                return

        if not transaction_id:
            error(lost_transaction_message)
            return

        if not (original_trans := self.trans_queue.get_transaction(transaction_id)):
            error(lost_transaction_message)
            return

        SvTerminal.reverse_transaction(self, original_trans)

    def parse_main_window(self) -> Transaction:
        data_fields: TypeFields = self.window.get_fields()

        if not data_fields:
            raise ValueError("No data to send")

        if not (message_type := self.window.get_mti(self.spec.MessageLength.message_type_length)):
            raise ValueError("Invalid MTI")

        transaction = Transaction(
            trans_id=self.generator.generate_trans_id(),
            message_type=message_type,
            max_amount=self.config.fields.max_amount,
            generate_fields=self.window.get_fields_to_generate(),
            data_fields=data_fields
        )

        return transaction

    def send(self, transaction: Transaction | None = None):
        if self.config.debug.clear_log:
            self.window.clean_window_log()

        if not transaction:
            try:
                transaction: Transaction = self.parse_main_window()

            except Exception as building_error:
                error(f"Transaction building error")
                [error(err) for err in str(building_error).splitlines()]
                return

        info(f"Processing transaction ID [{transaction.trans_id}]")

        SvTerminal.send(self, transaction)

        if self.sender() is self.window.button_send:
            self.set_generated_fields(transaction)

    @staticmethod
    def get_output_filename():
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        filename = file_dialog.getSaveFileName()[0]
        return filename

    def save_transaction_to_file(self, file_format: str) -> None:
        if not (filename := self.get_output_filename()):
            error("No output filename recognized")
            return

        try:
            transaction = self.parse_main_window()
        except Exception as file_saving_error:
            error("File saving error: %s", file_saving_error)
            return

        SvTerminal.save_transaction(self, transaction, file_format, filename)

    def print_data(self, data_format: str) -> None:
        if data_format not in DataFormats.get_print_data_formats():
            error("Wrong format of output data: %s", data_format)
            return

        data_processing_map = {
            DataFormats.JSON: lambda: dumps(self.parse_main_window().dict(), indent=4),
            DataFormats.DUMP: lambda: self.parser.create_sv_dump(self.parse_main_window()),
            DataFormats.INI: lambda: self.parser.transaction_to_ini_string(self.parse_main_window()),
            DataFormats.TERM: lambda: f"{TextConstants.HELLO_MESSAGE}",
            DataFormats.SPEC: lambda: dumps(self.spec.spec.dict(), indent=4)
        }

        if not (function := data_processing_map.get(data_format)):
            error(f"Wrong data format for printing: {data_format}")
            return

        try:
            self.window.set_log_data(function())
        except (ValidationError, ValueError, LookupError) as validation_error:
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
        reversal_window.exec()
        return reversal_window.reversal_id

    def set_default_values(self):
        try:
            self.parse_file(str(TermFilesPath.DEFAULT_FILE))
            info("Default file parsed")

        except Exception as parsing_error:
            error("Default file parsing error! Exception: %s" % parsing_error)

    def parse_file(self, filename: str | None = None) -> None:
        filename_found = ""

        if not filename:
            if not (filename := QFileDialog.getOpenFileName()[0]):
                info("No input filename recognized")
                return

            filename_found: str = filename

        try:
            transaction: Transaction = self.parser.parse_file(filename)
        except (TypeError, ValueError, Exception) as parsing_error:
            error(f"File parsing error: {parsing_error}")
            return

        if transaction.generate_fields:
            self.generator.set_generated_fields(transaction)
            self.set_generated_fields(transaction)

        try:
            self.window.set_mti_value(transaction.message_type)
            self.window.set_fields(transaction)
            self.set_bitmap()

        except ValueError as fields_settings_error:
            error(fields_settings_error)
            return

        if not filename_found:
            return

        info(f"File parsed: {filename}")

    def set_bitmap(self):
        bitmap: set[str] = set()

        for bit in self.window.get_top_level_field_numbers():
            if not bit.isdigit():
                continue

            if int(bit) not in range(1, self.spec.MessageLength.second_bitmap_capacity + 1):
                continue

            if not (self.window.get_field_data(bit) or bit in self.window.get_fields_to_generate()):
                continue

            if int(bit) >= self.spec.MessageLength.first_bitmap_capacity:
                bitmap.add(self.spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY)

            bitmap.add(bit)

        self.window.set_bitmap(", ".join(sorted(bitmap, key=int)))

    def clear_message(self):
        self.window.clear_message()
        self.set_bitmap()

    def set_generated_fields(self, transaction: Transaction):
        for field in transaction.generate_fields:

            if not self.spec.can_be_generated([field]):
                warning(f"According to specification Field {field} cannot be generated")
                continue

            if not transaction.data_fields.get(field):
                transaction.data_fields[field] = self.generator.generate_field(field)

            self.window.set_field_value(field, transaction.data_fields.get(field))
