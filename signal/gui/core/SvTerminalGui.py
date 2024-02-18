from typing import Callable
from logging import error, info, warning, Logger
from pydantic import ValidationError
from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtNetwork import QTcpSocket
from PyQt6.QtCore import Qt, pyqtSignal
from signal.gui.windows.main_window import MainWindow
from signal.gui.windows.reversal_window import ReversalWindow
from signal.gui.windows.settings_window import SettingsWindow
from signal.gui.windows.spec_window import SpecWindow
from signal.gui.windows.hotkeys_hint_window import HotKeysHintWindow
from signal.gui.windows.about_window import AboutWindow
from signal.gui.windows.complex_fields_window import ComplexFieldsParser
from signal.gui.windows.license_window import LicenseWindow
from signal.gui.core.WirelessHandler import WirelessHandler
from signal.gui.core.ConnectionThread import ConnectionThread
from signal.gui.enums import ButtonActions
from signal.gui.enums.Colors import Colors
from signal.lib.enums import KeepAlive
from signal.lib.enums.TermFilesPath import TermFilesPath
from signal.lib.enums.DataFormats import DataFormats, PrintDataFormats
from signal.lib.enums.MessageLength import MessageLength
from signal.lib.enums.TextConstants import TextConstants
from signal.lib.core.TransTimer import TransactionTimer
from signal.lib.core.SpecFilesRotator import SpecFilesRotator
from signal.lib.core.Logger import LogStream, getLogger, Formatter
from signal.lib.core.Terminal import SvTerminal
from signal.lib.data_models.Config import Config
from signal.lib.data_models.Transaction import Transaction, TypeFields
from signal.lib.constants import LogDefinition
from signal.lib.exceptions.exceptions import (
    LicenceAlreadyAccepted,
    LicenseDataLoadingError,
    DataValidationWarning,
    DataValidationError
)


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
    trans_timer: TransactionTimer = TransactionTimer(KeepAlive.TransTypes.TRANS_TYPE_TRANSACTION)
    set_remote_spec: pyqtSignal = pyqtSignal()
    startup_finished: pyqtSignal = pyqtSignal()
    wireless_handler: WirelessHandler
    _license_demonstrated: bool = False
    _startup_finished: bool = False

    def set_json_view_focus(function: callable):

        # This decorator sets focus on the self.window.json_view after the decorated function execution is finished

        def wrapper(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)

            finally:
                self.window.json_view.setFocus()

        return wrapper

    def __init__(self, config: Config):
        self.connector = ConnectionThread(config)
        super(SvTerminalGui, self).__init__(config, self.connector)
        self.window: MainWindow = MainWindow(self.config)
        self.setup()

    @set_json_view_focus
    def setup(self) -> None:
        self.log_printer.print_startup_info()
        self.create_window_logger()
        self.connect_widgets()
        self.window.set_mti_values(self.spec.get_mti_list())
        self.window.set_connection_status(QTcpSocket.SocketState.UnconnectedState)
        self.window.show()

    @set_json_view_focus
    def on_startup(self, app_state) -> None:
        if not app_state == Qt.ApplicationState.ApplicationActive:
            return

        if self._startup_finished:
            return

        self.print_data(DataFormats.TERM)

        if self.config.terminal.process_default_dump:
            self.set_default_values()

        if self.config.host.keep_alive_mode:
            interval: int = self.config.host.keep_alive_interval
            self.set_keep_alive_interval(interval_name=KeepAlive.IntervalNames.KEEP_ALIVE_DEFAULT % interval)

        if self.config.terminal.load_remote_spec:
            if not self.config.remote_spec.remote_spec_url:
                warning("Remote specification was not loaded due to empty spec URL")
                warning("The local specification will be used instead")

            if self.config.remote_spec.remote_spec_url:
                self.set_remote_spec.emit()

        if self.config.remote_spec.backup_storage:
            rotator: SpecFilesRotator = SpecFilesRotator()
            rotator.clear_spec_backup(self.config)

        if self.config.terminal.connect_on_startup:
            self.reconnect()

        self.window.enable_json_mode_checkboxes(enable=self.config.validation.validation_enabled)

        self._startup_finished: bool = True

    def connect_widgets(self):
        window: MainWindow = self.window

        terminal_connections_map: dict[pyqtSignal, Callable] = {

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
            window.repeat: self.trans_timer.set_trans_loop_interval,
            window.validate_message: self.validate_main_window,
            window.parse_complex_field: lambda: ComplexFieldsParser(self.config, self).exec(),
            self.connector.stateChanged: self.set_connection_status,
            self.set_remote_spec: self.connector.set_remote_spec,
            self.trans_timer.send_transaction: window.send,
            self.trans_timer.interval_was_set: window.process_transaction_loop_change,
            self.keep_alive_timer.interval_was_set: window.process_transaction_loop_change,
            self.startup_finished: self.log_printer.startup_finished,
        }

        for signal, slot in terminal_connections_map.items():
            signal.connect(slot)

        for slot in self.show_license_dialog, self.on_startup:
            self.pyqt_application.applicationStateChanged.connect(slot)

    def show_license_dialog(self, app_state) -> None:
        if app_state != Qt.ApplicationState.ApplicationActive:
            return

        if self._license_demonstrated:
            return

        try:
            license_window: LicenseWindow = LicenseWindow()
            license_window.exec()

        except LicenceAlreadyAccepted:
            self._license_demonstrated: bool = True
            return

        except LicenseDataLoadingError as license_data_loading_error:
            error(license_data_loading_error)
            exit(100)

        self._license_demonstrated: bool = True

    @set_json_view_focus
    def run_specification_window(self) -> None:
        spec_window: SpecWindow = SpecWindow(self.connector, self.config)
        getLogger().removeHandler(self.wireless_handler)
        spec_window.exec()
        getLogger().removeHandler(spec_window.wireless_handler)
        self.create_window_logger()

        if self.config.fields.hide_secrets:
            self.window.hide_secrets()

        if self.config.validation.validation_enabled:
            info("Validate message after spec settings")
            self.modify_fields_data()
            self.validate_main_window()

        if not self.config.validation.validation_enabled:
            self.window.refresh_fields(Colors.BLACK)

    def modify_fields_data(self):  #  Set extended data modifications, set in field params
        self.window.modify_fields_data()

    def validate_main_window(self, check_config: bool = True):
        if not self.config.validation.validation_enabled:
            error("Validation disabled in settings")
            self.window.refresh_fields(color=Colors.BLACK)
            return

        self.window.validate_fields(check_config=check_config)
        self.window.refresh_fields()
        info("Transaction data validated")

    def echo_test(self) -> None:
        try:
            SvTerminal.echo_test(self)

        except ValidationError as validation_error:
            error(validation_error.json())

        except Exception as sending_error:
            error(sending_error)

    @set_json_view_focus
    def settings(self) -> None:
        try:
            old_config: Config = self.config.model_copy(deep=True)
            settings_window: SettingsWindow = SettingsWindow(self.config)
            settings_window.accepted.connect(lambda: self.process_config_change(old_config))
            settings_window.exec()

        except Exception as settings_error:
            error(settings_error)

    def process_config_change(self, old_config: Config) -> None:
        self.read_config()

        if "" in (self.config.host.host, self.config.host.port):
            warning("Lost SV address or SV port! Check the parameters")

        try:
            if not self.config.host.port:
                raise ValueError

            if int(self.config.host.port) > 65535:
                raise ValueError

        except ValueError:
            warning(f"Incorrect SV port value: {self.config.host.port}. Must be a number in the range of 0 to 65535")

        info("Settings applied")

        self.window.enable_validation(self.config.validation.validation_enabled)
        self.window.enable_json_mode_checkboxes(enable=self.config.validation.validation_enabled)

        if old_config.validation.validation_enabled != self.config.validation.validation_enabled:
            if self.config.validation.validation_enabled:
                self.modify_fields_data()
                self.validate_main_window()

            if not self.config.validation.validation_enabled:
                self.window.refresh_fields(Colors.BLACK)

        if old_config.fields.json_mode != self.config.fields.json_mode:
            self.window.set_json_mode(self.config.fields.json_mode)

        if old_config.fields.hide_secrets != self.config.fields.hide_secrets:
            self.window.hide_secrets()

        spec_loading_conditions: list[bool] = [
            self.config.remote_spec.remote_spec_url,
            old_config.remote_spec.remote_spec_url != self.config.remote_spec.remote_spec_url,
        ]

        if all(spec_loading_conditions):
            try:
                self.validator.validate_url(self.config.remote_spec.remote_spec_url)

            except ValidationError as url_validation_error:
                error(f"Remote spec URL validation error: {url_validation_error}")

            else:
                self.set_remote_spec.emit()

        keep_alive_change_conditions: list[bool] = [
            old_config.host.keep_alive_mode != self.config.host.keep_alive_mode,
            old_config.host.keep_alive_interval != self.config.host.keep_alive_interval
        ]

        if any(keep_alive_change_conditions):
            interval_name: str = KeepAlive.IntervalNames.KEEP_ALIVE_STOP

            if self.config.host.keep_alive_mode:
                interval_name: str = KeepAlive.IntervalNames.KEEP_ALIVE_DEFAULT % self.config.host.keep_alive_interval

            self.set_keep_alive_interval(interval_name)

    def read_config(self) -> None:
        try:
            with open(TermFilesPath.CONFIG) as json_file:
                config: Config = Config.model_validate_json(json_file.read())

        except ValidationError as parsing_error:
            error(f"Cannot parse configuration file: {parsing_error}")
            return

        self.config.fields = config.fields

    def stop_sv_terminal(self) -> None:
        self.connector.stop_thread()

    def reconnect(self) -> None:
        SvTerminal.reconnect(self)

    def set_connection_status(self) -> None:
        self.window.set_connection_status(self.connector.state())

        if self.connector.state() is QTcpSocket.SocketState.ConnectingState:
            self.window.block_connection_buttons()
            return

        self.window.unblock_connection_buttons()

    def create_window_logger(self) -> None:
        formatter: Formatter = Formatter(LogDefinition.FORMAT, LogDefinition.DISPLAY_DATE_FORMAT, LogDefinition.MARK_STYLE)
        self.wireless_handler: WirelessHandler = WirelessHandler()
        stream: LogStream = LogStream(self.window.log_browser)
        self.wireless_handler.new_record_appeared.connect(lambda record: stream.write(data=record))
        self.wireless_handler.setFormatter(formatter)
        logger: Logger = getLogger()
        logger.addHandler(self.wireless_handler)

    def perform_reversal(self, command: str) -> None:
        transaction_source_map: dict[str, Callable] = {
            ButtonActions.ReversalMenuActions.LAST: self.trans_queue.get_last_reversible_transaction_id,
            ButtonActions.ReversalMenuActions.OTHER: self.show_reversal_window,
            ButtonActions.ReversalMenuActions.SET_REVERSAL: self.show_reversal_window,
        }

        try:
            if not (transaction_source := transaction_source_map.get(command)):
                raise LookupError

            if not (transaction_id := transaction_source()):
                raise LookupError

            if not (original_trans := self.trans_queue.get_transaction(transaction_id)):
                raise LookupError

            if not self.spec.get_reversal_mti(original_trans.message_type):
                raise LookupError

            if not (reversal := self.build_reversal(original_trans)):
                raise LookupError

        except Exception as reversal_building_error:
            error(f"Cannot reverse transaction, lost transaction ID or non-reversible MTI {reversal_building_error}")
            return

        match command:
            case ButtonActions.ReversalMenuActions.SET_REVERSAL:
                self.parse_transaction(reversal)

            case ButtonActions.ReversalMenuActions.LAST | ButtonActions.ReversalMenuActions.OTHER:
                try:
                    self.send(reversal)
                except Exception as sending_error:
                    error(sending_error)

            case _:
                error("Cannot reverse transaction")

    def parse_main_window(self, flat_fields: bool = True, clean: bool = False) -> Transaction:
        data_fields: TypeFields = self.window.get_fields(flat=flat_fields)

        if not data_fields:
            raise ValueError("No transaction data found")

        if not (message_type := self.window.get_mti(MessageLength.MESSAGE_TYPE_LENGTH)):
            raise ValueError("Invalid MTI")

        if self.config.validation.validation_enabled and self.validator.validate_fields(fields=data_fields):
            raise DataValidationError("Transaction aborted due to validation errors")

        try:
            transaction: Transaction = Transaction(
                generate_fields=self.window.get_fields_to_generate(),
                data_fields=data_fields,
                message_type=message_type,
                max_amount=self.config.fields.max_amount,
                is_reversal=self.spec.is_reversal(message_type)
            )

        except (ValidationError, ValueError) as validation_error:
            [error(err.get("msg")) for err in validation_error.errors()]
            raise DataValidationError

        if self.config.fields.send_internal_id:
            transaction: Transaction = self.generator.set_trans_id(transaction)

        if clean:
            del (
                transaction.resp_time_seconds,
                transaction.match_id,
                transaction.utrnno,
                transaction.matched,
                transaction.success,
                transaction.is_request,
                transaction.is_reversal,
                transaction.is_keep_alive,
                transaction.json_fields,
                transaction.sending_time,
            )

        return transaction

    def send(self, transaction: Transaction | None = None) -> None:
        if self.connector.connection_in_progress():
            error("Cannot send the transaction while the host connection is in progress")
            return

        if not transaction:
            try:
                transaction: Transaction = self.parse_main_window()
            except Exception as building_error:
                [error(err) for err in str(building_error).splitlines()]
                return

        if self.config.debug.clear_log and not transaction.is_keep_alive:
            self.window.clean_window_log()

        if not transaction.is_keep_alive:
            info(f"Processing transaction ID [{transaction.trans_id}]")

        if transaction.generate_fields:
            transaction: Transaction = self.generator.set_generated_fields(transaction)
            self.set_generated_fields(transaction)

        if self.config.fields.send_internal_id:
            transaction: Transaction = self.generator.set_trans_id(transaction)

        if self.config.validation.validation_enabled:
            try:
                self.validator.validate_transaction(transaction)

            except DataValidationError:
                error("Transaction aborted due to validation errors")
                return

            except Exception as validation_error:
                error(validation_error)
                return

        try:
            SvTerminal.send(self, transaction)  # SvTerminal always used to real data processing
        except Exception as sending_error:
            error(f"Transaction sending error: {sending_error}")
            return

    @staticmethod
    def get_output_filename() -> str:
        file_dialog: QFileDialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        filename: str = file_dialog.getSaveFileName()[0]
        return filename

    def save_transaction_to_file(self, file_format: str) -> None:
        if not (filename := self.get_output_filename()):
            error("No output filename recognized")
            return

        try:
            transaction: Transaction = self.parse_main_window(flat_fields=False, clean=True)
        except Exception as file_saving_error:
            error("File saving error: %s", file_saving_error)
            return

        SvTerminal.save_transaction(self, transaction, file_format, filename)

    def print_data(self, data_format: PrintDataFormats) -> None:
        data_processing_map: dict[str, Callable] = {
            DataFormats.JSON: lambda: self.parse_main_window(flat_fields=False, clean=True).model_dump_json(indent=4),
            DataFormats.DUMP: lambda: self.parser.create_sv_dump(self.parse_main_window()),
            DataFormats.INI: lambda: self.parser.transaction_to_ini_string(self.parse_main_window()),
            DataFormats.TERM: lambda: TextConstants.HELLO_MESSAGE + "\n",
            DataFormats.SPEC: lambda: self.spec.spec.model_dump_json(indent=4),
            DataFormats.CONFIG: lambda: self.config.model_dump_json(indent=4),
            ButtonActions.PrintButtonDataFormats.TRANS_DATA: self.print_trans_data,
        }

        if not (function := data_processing_map.get(data_format)):
            error(f"Wrong data format for printing: {data_format}")
            return

        try:
            self.window.set_log_data(function())
        except Exception as validation_error:
            error(f"{validation_error}")

    def print_trans_data(self):
        trans_id: str = self.show_reversal_window()
        transactions: list[Transaction] = list()

        if trans_id is None:
            raise ValueError("Cannot get transaction ID")

        if not (request := self.trans_queue.get_transaction(trans_id)):
            raise LookupError(f"Transaction lookup error {trans_id}")

        transactions.append(request)

        if request.matched:
            response = self.trans_queue.get_transaction(request.match_id)
            transactions.append(response)

        trans_data: str = ""

        for transaction in transactions:
            trans_data = f"{trans_data}\n{self.parser.transaction_to_ini_string(transaction)}"

        return trans_data

    def copy_log(self) -> None:
        self.set_clipboard_text(self.window.get_log_data())

    def copy_bitmap(self) -> None:
        self.set_clipboard_text(self.window.get_bitmap_data())

    @staticmethod
    def set_clipboard_text(data: str = str()) -> None:
        QApplication.clipboard().setText(data)

    def show_reversal_window(self) -> str:
        reversible_transactions_list: list[Transaction] = self.trans_queue.get_reversible_transactions()
        reversal_window: ReversalWindow = ReversalWindow(reversible_transactions_list)
        accepted: int = reversal_window.exec()

        if bool(accepted):
            return reversal_window.reversal_id

        raise LookupError

    @set_json_view_focus
    def set_default_values(self) -> None:
        try:
            self.parse_file(str(TermFilesPath.DEFAULT_FILE))
            info("Default file parsed")

        except Exception as parsing_error:
            error("Default file parsing error! Exception: %s" % parsing_error)

    @set_json_view_focus
    def parse_file(self, filename: str | None = None) -> None:
        filename_found: str = ""

        if not filename:
            if not (filename := QFileDialog.getOpenFileName()[0]):
                warning("No input filename recognized")
                return

            filename_found: str = filename

        try:
            transaction: Transaction = self.parser.parse_file(filename)

        except ValidationError as validation_error:
            error(f"File parsing error: {validation_error}")
            return

        except Exception as parsing_error:
            error(f"File parsing error: {parsing_error}")
            return

        if not transaction.max_amount:
            transaction.max_amount = self.config.fields.max_amount

        try:
            self.parse_transaction(transaction)

        except ValueError as fields_setting_error:
            error(fields_setting_error)
            return

        if not filename_found:
            return

        info(f"File parsed: {filename}")

    @set_json_view_focus
    def parse_transaction(self, transaction: Transaction) -> None:
        try:
            self.window.set_mti_value(transaction.message_type)
            self.window.set_transaction_fields(transaction)
            self.set_bitmap()

        except DataValidationWarning as validation_warning:
            [warning(warn) for warn in str(validation_warning).splitlines()]

        except Exception as transaction_parsing_error:
            error(f"Cannot set transaction fields: {transaction_parsing_error}")
            return

        if self.config.validation.validation_enabled:
            self.modify_fields_data()

    def set_bitmap(self) -> None:
        bitmap: set[str] = set()

        for bit in self.window.get_top_level_field_numbers():
            if not bit.isdigit():
                continue

            if int(bit) not in range(1, MessageLength.SECOND_BITMAP_CAPACITY + 1):
                continue

            if not (self.window.field_has_data(bit) or bit in self.window.get_fields_to_generate()):
                continue

            if int(bit) >= MessageLength.FIRST_BITMAP_CAPACITY:
                bitmap.add(self.spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY)

            bitmap.add(bit)

        self.window.set_bitmap(", ".join(sorted(bitmap, key=int)))

    @set_json_view_focus
    def clear_message(self) -> None:
        self.window.clear_message()
        self.set_bitmap()

    def set_generated_fields(self, transaction: Transaction) -> None:
        for field in transaction.generate_fields:

            if not self.spec.can_be_generated([field]):
                continue

            if not transaction.data_fields.get(field):
                transaction.data_fields[field]: str = self.generator.generate_field(field)

            self.window.set_field_value(field, transaction.data_fields.get(field))
