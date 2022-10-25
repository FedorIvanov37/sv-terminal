from json import dumps
from logging import error, info
from PyQt5.Qt import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtNetwork import QTcpSocket
from PyQt5 import QtWidgets
from pydantic import ValidationError
from common.app.core.windows.main_window import MainWindow
from common.app.core.windows.reversal_window import ReversalWindow
from common.app.core.windows.settings_window import SettingsWindow
from common.app.core.windows.spec_window import SpecWindow
from common.app.core.tools.parser import Parser
from common.app.core.tools.logger import Logger
from common.app.core.tools.transaction_queue import TransactionQueue
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.core.tools.connector import ConnectionWorker
from common.app.core.tools.fields_generator import FieldsGenerator
from common.app.core.tools.validator import Validator
from common.app.constants.TextConstants import TextConstants
from common.app.constants.DataFormats import DataFormats
from common.app.constants.FilePath import FilePath
from common.app.data_models.config import Config
from common.app.data_models.transaction import Transaction


class SvTerminal(QObject):
    _config: Config = Config.parse_file(FilePath.CONFIG)
    _pyqt_application = QtWidgets.QApplication([])
    _validator = Validator(_config)
    _need_reconnect: pyqtSignal = pyqtSignal()
    _spec: EpaySpecification = EpaySpecification()
    _new_connector: ConnectionWorker
    _connection_thread: QThread
    _send_transaction: pyqtSignal = pyqtSignal(Transaction)

    @property
    def config(self):
        return self._config

    @property
    def validator(self):
        return self._validator

    @property
    def new_connector(self):
        return self._new_connector

    @new_connector.setter
    def new_connector(self, new_connector):
        self._new_connector = new_connector

    @property
    def spec(self):
        return self._spec

    def __init__(self):
        super(SvTerminal, self).__init__()
        self.parser: Parser = Parser(self.config)
        self.generator = FieldsGenerator(self.config)
        self.connector: ConnectionWorker = ConnectionWorker(self.config)
        self.window: MainWindow = MainWindow(self.config, self)
        self.logger: Logger = Logger(self.window.log_browser, self.config)
        self.trans_queue: TransactionQueue = TransactionQueue(self.config)
        self._connection_thread: QThread = QThread()
        self.start_connection_thread()

        if self.config.terminal.connect_on_startup:
            self.reconnect()

    def run(self):
        self.window.show()
        exit(self._pyqt_application.exec_())

    def start_connection_thread(self):
        self.connector.moveToThread(self._connection_thread)
        self._need_reconnect.connect(self.connector.connect_sv)
        self._send_transaction.connect(self.connector.send_transaction)
        self._connection_thread.started.connect(self.connector.run)
        self.connector.connected.connect(lambda: self.window.set_connection_status(QTcpSocket.ConnectedState))
        self.connector.disconnected.connect(lambda: self.window.set_connection_status(QTcpSocket.UnconnectedState))
        self.connector.socker_error.connect(lambda err: self.socket_error())
        self.connector.connection_started.connect(self.window.lock_connection_buttons)
        self.connector.connection_finished.connect(lambda: self.window.lock_connection_buttons(lock=False))
        self.connector.ready_read.connect(self.read_from_socket)
        self._connection_thread.start()

    def socket_error(self):
        if self.connector.error() == -1:  # TODO
            return
        
        error("Received socket error: %s", self.connector.error_string())

    def send(self, transaction: Transaction):
        if self.config.debug.clear_log:
            self.window.clear_log()

        if transaction.generate_fields:
            transaction: Transaction = self.generator.set_generated_fields(transaction)

        if not transaction.trans_id:
            transaction.trans_id = self.generator.trans_id()

        if self.config.fields.send_internal_id:
            transaction: Transaction = self.generator.set_trans_id_to_47_072(transaction)

        if self.sender() is self.window.button_send:
            self.window.set_generated_fields(transaction)

        if self.config.fields.validation:
            try:
                self.validator.validate_transaction(transaction)
            except (ValueError, TypeError) as validation_error:
                error(f"Transaction validation error {validation_error}")
                return

        self.logger.print_dump(transaction)
        self.trans_queue.put_transaction(transaction)
        info(f"Processing transaction with internal ID [{transaction.trans_id}]")
        self.logger.print_transaction(transaction)
        self._send_transaction.emit(transaction)

    def settings(self):
        SettingsWindow(self.config).exec_()

    def specification(self):
        spec_window: SpecWindow = SpecWindow(self.window)
        spec_window.spec_accepted.connect(lambda: info("Specification accepted"))
        spec_window.exec_()

    def save_transaction_to_file(self, transaction: Transaction, filename: str, file_format: str) -> None:
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

    def disconnect(self):
        self.connector.disconnect_sv()

    def reconnect(self):
        info("[Re]connecting...")
        self._need_reconnect.emit()

    def read_from_socket(self):
        data = self.connector.read_from_socket().data()

        try:
            transaction: Transaction = self.parser.parse_dump(data=data)
        except Exception as parsing_error:
            error("Incoming transaction parsing error: %s", parsing_error)
            return

        self.trans_queue.put_response(response=transaction)
        self.logger.print_dump(transaction)
        self.logger.print_transaction(transaction)

    def print_data(self, data_format: str) -> None:
        if data_format not in DataFormats.get_print_data_formats():
            error("Wrong format of output data: %s", data_format)
            return

        data_processing_map = {
            DataFormats.JSON: lambda: dumps(self.parser.parse_form(self.window).dict(), indent=4),
            DataFormats.DUMP: lambda: self.parser.create_sv_dump(self.parser.parse_form(self.window)),
            DataFormats.INI: lambda: self.parser.transaction_to_ini_string(self.parser.parse_form(self.window)),
            DataFormats.SV_TERMINAL: lambda: TextConstants.HELLO_MESSAGE,
            DataFormats.SPEC: lambda: dumps(self.spec.spec.dict(), indent=4)
        }

        if not (function := data_processing_map.get(data_format)):
            error(f"Wrong data format for printing: {data_format}")
            return

        try:
            self.window.log_browser.setText(function())
        except ValidationError as validation_error:
            error(f"{validation_error}")

    @staticmethod
    def set_clipboard_text(data: str) -> None:
        QApplication.clipboard().setText(data)

    def get_last_reversible_transaction_id(self):
        if not (transaction_id := self.trans_queue.get_last_reversible_transaction_id()):
            error("Transaction Queue has no reversible transactions")

        return transaction_id

    def show_reversal_window(self):
        reversible_transactions_list: list[Transaction] = self.trans_queue.get_reversible_transactions()
        reversal_window = ReversalWindow(reversible_transactions_list)

        if reversal_window.exec_():
            if not reversal_window.reversal_id:
                error("No transaction ID recognized. The Reversal wasn't sent")

            return reversal_window.reversal_id

        info("Reversal sending is cancelled by user")

    def reverse_transaction(self, original_transaction_id: str):
        original: Transaction = self.trans_queue.get_transaction(original_transaction_id)
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
