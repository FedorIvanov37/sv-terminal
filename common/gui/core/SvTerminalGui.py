from json import dumps
from logging import error, info, warning
from pydantic import ValidationError
from PyQt6.QtWidgets import QApplication
from PyQt6.QtNetwork import QTcpSocket
from PyQt6.QtWidgets import QFileDialog
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
from common.gui.core.WirelessHandler import WirelessHandler
from common.gui.core.ConnectionThread import ConnectionThread
from common.lib.core.Logger import LogStream, getLogger, Formatter
from common.lib.constants.LogDefinition import LogDefinition
from common.lib.data_models.Config import Config
from common.lib.data_models.Transaction import Transaction, TypeFields
from common.lib.core.Terminal import SvTerminal


"""
 
 The core of the GUI backend
 
 Performs all the management and control. The main purpose is to receive a validated data-processing request from 
 MainWindow or TransactionQueue and manage this using the other low-level modules such as Parser for data transformation
 TransactionQueue for interaction with the target system, Connector for TCP integration, and so on. 
 
 Always tries not to do the work itself, managing corresponding modules instead

 SvTerminalGui is a basic executor for all user requests. Inherited from SvTerminal class, which does not interact 
 with GUI anyhow. Low-level data processing performs using the basic SvTerminal class.

 Usually get data in the Transaction format. In any other case targeting to transform data into the Transaction and 
 proceed to work with this. The Transaction is a common I/O format for SvTerminalGui. 
 
 Starts MainWindow when starting its work, being a kind of low-level adapter between the GUI and the system's core
 
"""


class SvTerminalGui(SvTerminal):
    connector: ConnectionThread

    def __init__(self, config: Config):
        super(SvTerminalGui, self).__init__(config, ConnectionThread(config))
        self.window: MainWindow = MainWindow(self.config)
        self.setup()

    def setup(self):
        self.create_window_logger()
        self.log_printer.print_startup_info()
        self.connect_widgets()
        self.window.set_mti_values(self.spec.get_mti_list())
        self.window.set_connection_status(QTcpSocket.SocketState.UnconnectedState)
        self.print_data(DataFormats.TERM)

        if self.config.terminal.process_default_dump:
            self.set_default_values()

        if self.config.smartvista.keep_alive_mode:
            interval = self.config.smartvista.keep_alive_interval
            self.switch_keep_alive_mode(interval_name=ButtonAction.KEEP_ALIVE_DEFAULT % interval)

        self.window.show()

    def connect_widgets(self):
        window = self.window

        terminal_connections_map = {

            # Data processing request channels. Usually get the tasks from MainWindow or low-level SvTerminal

            window.clear_log: window.clean_window_log,
            window.send: self.send,
            window.reset: self.set_default_values,
            window.echo_test: self.echo_test,
            window.clear: self.clear_message,
            window.copy_log: self.copy_log,
            window.copy_bitmap: self.copy_bitmap,
            window.reconnect: self.reconnect,
            window.parse_file: self.parse_file,
            window.window_close: self.stop_sv_terminal,
            window.reverse: self.perform_reversal,
            window.print: self.print_data,
            window.save: self.save_transaction_to_file,
            window.field_changed: self.set_bitmap,
            window.field_removed: self.set_bitmap,
            window.field_added: self.set_bitmap,
            window.settings: self.settings,
            window.hotkeys: lambda: HotKeysHintWindow().exec(),
            window.specification: lambda: SpecWindow().exec(),
            window.about: lambda: AboutWindow(),
            window.keep_alive: self.switch_keep_alive_mode,
            self.connector.stateChanged: self.set_connection_status,
        }

        for signal, slot in terminal_connections_map.items():
            signal.connect(slot)

    def settings(self):
        def validate_all(validation: bool):
            if not validation:  # Return when no changes detected
                return

            self.window.validate_fields()

        def set_keep_alive(keep_alive_mode_changed: bool):
            if not keep_alive_mode_changed:  # Return when no changes detected
                return

            interval_name = ButtonAction.KEEP_ALIVE_STOP

            if self.config.smartvista.keep_alive_mode:
                interval_name = ButtonAction.KEEP_ALIVE_DEFAULT % self.config.smartvista.keep_alive_interval

            self.switch_keep_alive_mode(interval_name)

        # Save configuration to local variables for future compare to track changes
        fields_validation = self.config.fields.validation
        keep_alive = self.config.smartvista.keep_alive_mode

        settings_window: SettingsWindow = SettingsWindow(self.config)
        settings_window.accepted.connect(self.read_config)
        settings_window.accepted.connect(lambda: validate_all(fields_validation != self.config.fields.validation))
        settings_window.accepted.connect(lambda: set_keep_alive(keep_alive != self.config.smartvista.keep_alive_mode))
        settings_window.accepted.connect(lambda: self.window.set_json_mode(self.config.fields.json_mode))
        settings_window.exec()

    def read_config(self):
        config = Config.parse_file(TermFilesPath.CONFIG)
        self.config.fields = config.fields

    def stop_sv_terminal(self):
        self.connector.stop_thread()

    def switch_keep_alive_mode(self, interval_name):
        if interval_name == ButtonAction.KEEP_ALIVE_ONCE:
            self.keep_alive()
            return

        if interval_name == ButtonAction.KEEP_ALIVE_STOP:
            self.keep_alive_timer.stop()
            self.window.process_keep_alive_change(interval_name)
            return

        interval = None
        keep_alive_default = ButtonAction.KEEP_ALIVE_DEFAULT % self.config.smartvista.keep_alive_interval

        if interval_name == keep_alive_default:
            info(f"Set KeepAlive mode to {interval_name}")
            interval = self.config.smartvista.keep_alive_interval

        if interval is None:
            if not (interval := ButtonAction.get_interval_time(interval_name)):
                return

            info(f"Set KeepAlive mode to {interval_name}")

        self.window.process_keep_alive_change(interval_name)
        self.run_keep_alive_loop(int(interval))

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

        transaction_source_map = {
            ButtonAction.LAST: self.trans_queue.get_last_reversible_transaction_id,
            ButtonAction.OTHER: self.show_reversal_window
        }

        if not (transaction_source := transaction_source_map.get(id_source)):
            error(lost_transaction_message)
            return

        if not (transaction_id := transaction_source()):
            error(lost_transaction_message)
            return

        if not (original_trans := self.trans_queue.get_transaction(transaction_id)):
            error(lost_transaction_message)
            return

        SvTerminal.reverse_transaction(self, original_trans)

    def parse_main_window(self) -> Transaction:
        data_fields: TypeFields = self.window.get_fields()

        if not data_fields:
            raise ValueError("No transaction data found")

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
        sender = None

        if not transaction:
            try:
                transaction: Transaction = self.parse_main_window()
                sender = self.window

            except Exception as building_error:
                error(f"Transaction building error")
                [error(err) for err in str(building_error).splitlines()]
                return

        if self.config.debug.clear_log and not transaction.is_keep_alive:
            self.window.clean_window_log()

        if not transaction.is_keep_alive:
            info(f"Processing transaction ID [{transaction.trans_id}]")

        SvTerminal.send(self, transaction)  # SvTerminal always used to real data processing

        if sender is self.window:
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
                warning("No input filename recognized")
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
                continue

            if not transaction.data_fields.get(field):
                transaction.data_fields[field] = self.generator.generate_field(field)

            self.window.set_field_value(field, transaction.data_fields.get(field))
