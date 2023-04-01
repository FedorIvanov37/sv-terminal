from json import dumps
from logging import error, info
from pydantic import ValidationError
from PyQt6.QtWidgets import QApplication
from PyQt6.QtNetwork import QTcpSocket
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QIcon
from common.gui.windows.main_window import MainWindow
from common.gui.windows.reversal_window import ReversalWindow
from common.gui.windows.settings_window import SettingsWindow
from common.gui.windows.spec_window import SpecWindow
from common.gui.core.logger import LogStream, getLogger, Formatter
from common.gui.constants.TextConstants import TextConstants
from common.gui.constants.DataFormats import DataFormats
from common.gui.constants.TermFilesPath import TermFilesPath
from common.lib.data_models.Config import Config
from common.lib.data_models.Transaction import Transaction
from common.gui.constants.ButtonActions import ButtonAction
from common.lib.core.Terminal import SvTerminal
from common.gui.core.wireless_log_handler import WirelessHandler
from common.gui.constants.LogDefinition import LogDefinition
from common.gui.core.connection_thread import ConnectionThread


class SvTerminalGui(SvTerminal):
    def __init__(self, config: Config):
        super(SvTerminalGui, self).__init__(config, ConnectionThread(config))
        self.window: MainWindow = MainWindow(self.config)
        self.setup()

    def setup(self):
        self.connect_widgets()
        self.create_window_logger()
        self.window.set_mti_values(self.spec.get_mti_list())
        self.window.set_log_data(TextConstants.HELLO_MESSAGE)
        self.window.setWindowIcon(QIcon(TermFilesPath.MAIN_LOGO))
        self.window.set_connection_status(QTcpSocket.SocketState.UnconnectedState)
        self.connector.errorOccurred.connect(self.set_connection_status)
        self.connector.errorOccurred.connect(self.window.unblock_connection_buttons)

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

        self.window.window_close.connect(self.stop_sv_terminal)
        self.window.menu_button_clicked.connect(self.proces_button_menu)
        self.window.field_changed.connect(self.set_bitmap)
        self.connector.stateChanged.connect(self.set_connection_status)

    def stop_sv_terminal(self):
        self.connector.disconnect_sv()
        self.connector.stop_thread()

    def reconnect(self):
        SvTerminal.reconnect(self)
        self.window.block_connection_buttons()

    def set_connection_status(self):
        connection_status = self.connector.state()

        if connection_status == QTcpSocket.SocketState.ConnectedState:
            self.window.unblock_connection_buttons()

        self.window.set_connection_status(connection_status)

    def create_window_logger(self):
        formatter = Formatter(LogDefinition.FORMAT, LogDefinition.DATE_FORMAT, LogDefinition.MARK_STYLE)
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

    def send(self, transaction: Transaction | None = None):
        if self.config.debug.clear_log:
            self.window.clear_log()

        if not transaction:
            try:
                transaction: Transaction = self.parser.parse_main_window(self.window)
            except Exception as building_error:
                error(f"Transaction building error")
                [error(err.strip()) for err in str(building_error).splitlines()]
                return

        info(f"Processing transaction ID [{transaction.trans_id}]")

        SvTerminal.send(self, transaction)

        if self.sender() is self.window.button_send:
            self.set_generated_fields(transaction)

    def settings(self):
        SettingsWindow(self.config).exec()

    def specification(self):
        spec_window: SpecWindow = SpecWindow(self.window)
        spec_window.spec_accepted.connect(lambda: info("Specification accepted"))
        spec_window.exec()

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
            transaction = self.parser.parse_main_window(self.window)
        except Exception as file_saving_error:
            error("File saving error: %s", file_saving_error)
            return

        SvTerminal.save_transaction(self, transaction, file_format, filename)

    def print_data(self, data_format: str) -> None:
        if data_format not in DataFormats.get_print_data_formats():
            error("Wrong format of output data: %s", data_format)
            return

        data_processing_map = {
            DataFormats.JSON: lambda: dumps(self.parser.parse_main_window(self.window).dict(), indent=4),
            DataFormats.DUMP: lambda: self.parser.create_sv_dump(self.parser.parse_main_window(self.window)),
            DataFormats.INI: lambda: self.parser.transaction_to_ini_string(self.parser.parse_main_window(self.window)),
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
        reversal_window.exec()
        return reversal_window.reversal_id

    def set_default_values(self):
        try:
            self.parse_file(str(TermFilesPath.DEFAULT_FILE))
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

        try:
            self.window.set_mti_value(transaction.message_type)
            self.window.set_fields(transaction)
            self.set_bitmap()

        except ValueError as fields_settings_error:
            error(fields_settings_error)
            return

        if self.sender() is self.window.button_parse_file:
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

    def proces_button_menu(self, button, action: str):
        data_processing_map = {
            self.window.button_save: lambda _action: self.save_transaction_to_file(_action),
            self.window.button_reverse: lambda _action: self.perform_reversal(_action),
            self.window.button_print: lambda _action: self.print_data(_action)
        }

        if not (function := data_processing_map.get(button)):
            return

        function(action)

    def clear_message(self):
        self.window.clear_message()
        self.set_bitmap()

    def set_generated_fields(self, transaction: Transaction):
        for field in transaction.generate_fields:
            if not transaction.data_fields.get(field):
                error("Lost field data for field %s")

            if not self.spec.can_be_generated([field]):
                error(f"Field {field} cannot be generated")
                return

            self.window.set_field_value(field, transaction.data_fields.get(field))
