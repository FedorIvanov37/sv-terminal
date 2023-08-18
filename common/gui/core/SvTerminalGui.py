from json import dumps
from copy import deepcopy
from logging import error, info, warning
from pydantic import ValidationError
from PyQt6.QtWidgets import QApplication
from PyQt6.QtNetwork import QTcpSocket
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QTimer
from common.gui.windows.main_window import MainWindow
from common.gui.windows.reversal_window import ReversalWindow
from common.gui.windows.settings_window import SettingsWindow
from common.gui.windows.spec_window import SpecWindow
from common.gui.windows.hotkeys_hint_window import HotKeysHintWindow
from common.gui.windows.about_window import AboutWindow
from common.lib.constants.TextConstants import TextConstants
from common.lib.constants.DataFormats import DataFormats
from common.lib.constants.TermFilesPath import TermFilesPath
from common.gui.constants.ButtonActions import ButtonAction
from common.lib.constants.KeepAliveIntervals import KeepAliveInterval
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
    trans_loop_timer: QTimer = QTimer()

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
            self.set_keep_alive_interval(interval_name=KeepAliveInterval.KEEP_ALIVE_DEFAULT % interval)

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
            window.specification: self.run_specification_window,
            window.about: lambda: AboutWindow(),
            window.keep_alive: self.set_keep_alive_interval,
            window.repeat: self.set_trans_loop_interval,
            self.connector.stateChanged: self.set_connection_status,
        }

        for signal, slot in terminal_connections_map.items():
            signal.connect(slot)

    def run_specification_window(self):
        spec_window = SpecWindow()
        spec_window.accepted.connect(self.window.hide_secrets)
        spec_window.exec()

    def activate_transaction_loop(self, interval: int):
        self.stop_transaction_loop()
        self.trans_loop_timer = QTimer()
        self.trans_loop_timer.timeout.connect(self.auto_send_transaction)
        self.trans_loop_timer.start(int(interval) * 1000)
        info(f"Transaction repeat set to {interval} second(s)")

    def stop_transaction_loop(self):
        self.trans_loop_timer.stop()
        info("Transaction repeat stopped")

    def set_trans_loop_interval(self, interval_name: str):
        if interval_name == KeepAliveInterval.KEEP_ALIVE_STOP:
            self.stop_transaction_loop()

        if interval := KeepAliveInterval.get_interval_time(interval_name):
            self.activate_transaction_loop(interval)

        self.window.process_repeat_change(interval_name)

    def auto_send_transaction(self):
        try:
            transaction: Transaction = self.parse_main_window()

        except Exception as window_parsing_error:
            error(f"MainWindow parsing error: {window_parsing_error}")
            return

        try:
            self.send(transaction)
        except Exception as sending_error:
            error(f"Transaction sending error: {sending_error}")

    def echo_test(self):
        try:
            SvTerminal.echo_test(self)

        except ValidationError as validation_error:
            error(validation_error.json())

        except Exception as sending_error:
            error(sending_error)

    def settings(self):
        old_config: Config = Config.parse_obj(deepcopy(self.config.dict()))
        settings_window: SettingsWindow = SettingsWindow(self.config)
        settings_window.accepted.connect(lambda: self.process_config_change(old_config))
        settings_window.exec()

    def process_config_change(self, old_config: Config):
        self.read_config()

        if "" in (self.config.smartvista.host, self.config.smartvista.port):
            warning("Lost SV address or SV port! Check the parameters")

        try:
            if not self.config.smartvista.port:
                raise ValueError

            if int(self.config.smartvista.port) > 65535:
                raise ValueError

        except ValueError:
            warning(f'Incorrect SV port value: "{self.config.smartvista.port}". '
                    f'Must be a number in the range of 0 to 65535')

        if old_config.fields.validation != self.config.fields.validation:
            self.window.validate_fields()

        if old_config.fields.json_mode != self.config.fields.json_mode:
            self.window.set_json_mode(self.config.fields.json_mode)

        if old_config.fields.hide_secrets != self.config.fields.hide_secrets:
            self.window.hide_secrets()

        if old_config.smartvista.keep_alive_mode != self.config.smartvista.keep_alive_mode:
            interval_name = KeepAliveInterval.KEEP_ALIVE_STOP

            if self.config.smartvista.keep_alive_mode:
                interval_name = KeepAliveInterval.KEEP_ALIVE_DEFAULT % self.config.smartvista.keep_alive_interval

            self.set_keep_alive_interval(interval_name)

        info("Settings applied")

    def read_config(self):
        try:
            config = Config.parse_file(TermFilesPath.CONFIG)
        except ValidationError as parsing_error:
            error(f"Cannot parse configuration file: {parsing_error}")
            return

        self.config.fields = config.fields

    def stop_sv_terminal(self):
        self.connector.stop_thread()


    def set_keep_alive_interval(self, interval_name: str):
        SvTerminal.set_keep_alive_interval(self, interval_name)
        self.window.process_keep_alive_change(interval_name)

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

        except ValidationError as validation_error:
            error(f"File parsing error: {validation_error.json()}")
            return

        except Exception as parsing_error:
            error(f"File parsing error: {parsing_error}")
            return

        if transaction.max_amount:
            self.config.fields.max_amount = transaction.max_amount

        if not transaction.max_amount:
            transaction.max_amount = self.config.fields.max_amount

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
