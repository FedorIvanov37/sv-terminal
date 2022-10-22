from PyQt5.Qt import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtNetwork import QTcpSocket
from json import dumps
from logging import error, info, debug
from common.app.core.windows.main_window import MainWindow
from common.app.core.windows.reversal_window import ReversalWindow
from common.app.core.windows.settings_window import SettingsWindow
from common.app.core.windows.spec_window import SpecWindow
from common.app.core.tools.parser import Parser
from common.app.core.tools.logger import Logger
from common.app.core.tools.transaction_queue import TransactionQueue
from common.app.data_models.config import Config
from common.app.constants.DataFormats import DataFormats
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.constants.TextConstants import TextConstants
from common.app.data_models.message import Message
from common.app.data_models.message import TransactionModel
from common.app.core.tools.connector import ConnectionWorker
from common.app.core.tools.fields_generator import FieldsGenerator
from common.app.core.tools.api.api import TerminalApi
from common.app.core.tools.validator import Validator


class Terminal(QObject):
    _message_ready: pyqtSignal = pyqtSignal(Message)
    _need_reconnect: pyqtSignal = pyqtSignal()
    _spec: EpaySpecification = EpaySpecification()
    _new_connector: ConnectionWorker
    _connection_thread: QThread
    _send_message: pyqtSignal = pyqtSignal(Message)

    @property
    def new_connector(self):
        return self._new_connector

    @new_connector.setter
    def new_connector(self, new_connector):
        self._new_connector = new_connector

    @property
    def spec(self):
        return self._spec

    @property
    def message_ready(self):
        return self._message_ready

    def __init__(self, config: Config):
        super(Terminal, self).__init__()
        self.config: Config = config
        self.parser: Parser = Parser(self.config)
        self.generator = FieldsGenerator(self.config)
        self.connector: ConnectionWorker = ConnectionWorker(self.config)
        self.window: MainWindow = MainWindow(self.config, self)
        self.logger: Logger = Logger(self.window.log_browser, self.config)
        self.trans_queue: TransactionQueue = TransactionQueue(self.config)
        self.api: TerminalApi = TerminalApi(self.config)
        self.api.adapter.message_ready.connect(lambda message: self.process_api_call(message))
        self.validator = Validator()

        # Working with connection thread
        self._connection_thread: QThread = QThread()
        self.connector = ConnectionWorker(self.config)
        self.connector.moveToThread(self._connection_thread)
        self._need_reconnect.connect(self.connector.connect_sv)
        self._send_message.connect(self.connector.send_message)
        self.connector.message_sent.connect(self.trans_queue.start_transaction_timer)
        self._connection_thread.started.connect(self.connector.run)
        self.connector.connected.connect(lambda: self.window.set_connection_status(QTcpSocket.ConnectedState))
        self.connector.disconnected.connect(lambda: self.window.set_connection_status(QTcpSocket.UnconnectedState))
        self.connector.socker_error.connect(lambda err: self.socket_error())
        self.connector.connection_started.connect(self.window.lock_connection_buttons)
        self.connector.connection_finished.connect(lambda: self.window.lock_connection_buttons(lock=False))
        self.connector.ready_read.connect(self.read_from_socket)
        self._connection_thread.start()

    def run_http_server(self):
        from common.app.core.tools.api.http_api import Adapter, FastApiApp
        self.adapter = Adapter()
        self.adapter.got_incoming_message.connect(lambda m: self.send(m))

        # from common.app.core.tools.api.http_api import run_app
        # run_app()

    def process_api_call(self, data: Message) -> None:
        self.send(data)

    def run(self):  # Start the terminal
        self.setup()
        self.window.show()

    def setup(self):
        if self.config.terminal.connect_on_startup:
            self.reconnect()

        self.logger.print_config(level=debug)
        info("Startup finished")

    def run_api(self):
        ...

    def stop_api(self):
        ...

    def socket_error(self):
        if self.connector.error() == -1:  # TODO
            return
        
        error("Received socket error: %s", self.connector.error_string())

    def send(self, message: Message):
        if self.config.debug.clear_log:
            self.window.clear_log()

        if message.config.generate_fields:
            message: Message = self.generator.set_generated_fields(message)

        if not message.transaction.id:
            message.transaction.id = self.generator.trans_id()

        if self.config.fields.send_internal_id:
            message: Message = self.generator.set_trans_id_to_47_072(message)

        if self.sender() is self.window.button_send:
            self.window.set_generated_fields(message)

        if self.config.fields.validation:
            try:
                self.validator.validate_message(message)
            except (ValueError, TypeError) as validation_error:
                error(f"Transaction validation error {validation_error}")
                return

        self.logger.print_dump(message)
        self.trans_queue.create_transaction(request=message)
        info(f"Processing transaction with internal ID [{message.transaction.id}]")
        self.logger.print_message(message)
        self._send_message.emit(message)

    def settings(self):
        SettingsWindow(self.config).exec_()

    def specification(self):
        spec_window: SpecWindow = SpecWindow(self.window)
        spec_window.spec_accepted.connect(lambda: info("Specification accepted"))
        spec_window.exec_()

    def save_message_to_file(self, message: Message, filename: str, file_format: str) -> None:
        data_processing_map = {
            DataFormats.JSON: lambda _message: dumps(_message.dict(), indent=4),
            DataFormats.INI: lambda _message: self.parser.get_transaction_data_ini(_message, string=True),
            DataFormats.DUMP: lambda _message: self.parser.create_sv_dump(_message)[1:]
        }

        if not (data_processing_function := data_processing_map.get(file_format)):
            error("Unknown output file format")
            return

        if not (file_data := data_processing_function(message)):
            error("No data to save")
            return

        with open(filename, "w") as file:
            file.write(file_data)

        info(f"The message was saved successfully to {filename}")

    def disconnect(self):
        self.connector.disconnect_sv()

    def reconnect(self):
        info("[Re]connecting...")
        self._need_reconnect.emit()

    def read_from_socket(self):
        data = self.connector.read_from_socket().data()

        try:
            message: Message = self.parser.parse_dump(data=data)
        except Exception as parsing_error:
            error("Incoming message parsing error: %s", parsing_error)
            return

        self.trans_queue.put_response_message(response=message)
        self.logger.print_dump(message)
        self.logger.print_message(message)

    def print_data(self, data_format: str) -> None:
        if data_format not in DataFormats.get_print_data_formats():
            error("Wrong format of output data: %s", data_format)
            return

        data_processing_map = {
            DataFormats.JSON: lambda: dumps(self.parser.parse_form(self.window).dict(), indent=4),
            DataFormats.DUMP: lambda: self.parser.create_sv_dump(self.parser.parse_form(self.window)),
            DataFormats.INI: lambda: self.parser.get_transaction_data_ini(self.parser.parse_form(self.window), string=True),
            DataFormats.SV_TERMINAL: lambda: TextConstants.HELLO_MESSAGE,
            DataFormats.SPEC: lambda: dumps(self.spec.spec.dict(), indent=4)
        }

        from pydantic import ValidationError

        if not (function := data_processing_map.get(data_format)):
            error(f"Wrong data format for printing: {data_format}")
            return

        try:
            self.window.log_browser.setText(function())
        except ValidationError as validation_error:
            error(f"{validation_error}")

    def get_last_reversible_transaction_id(self):
        transaction_id = None

        try:
            transaction_id = max(transaction.trans_id for transaction in self.get_reversible_transactions())
        except ValueError:
            error("Transaction Queue has no reversible transactions")

        return transaction_id

    def get_reversible_transactions(self):
        return self.trans_queue.get_reversible_transactions()

    def show_reversal_window(self):
        transaction_list: list = self.get_reversible_transactions()
        reversal_window = ReversalWindow(transaction_list)

        if reversal_window.exec_():
            if not reversal_window.reversal_id:
                error("No transaction ID recognized. The Reversal wasn't sent")

            return reversal_window.reversal_id

        info("Reversal sending is cancelled by user")

    @staticmethod
    def set_clipboard_text(data: str) -> None:
        QApplication.clipboard().setText(data)

    def reverse_transaction(self, original_transaction_id: str):
        if not (reversal_message := self.build_reversal(original_transaction_id)):
            error("Cannot build reversal")
            return

        self.send(reversal_message)

    def build_reversal(self, original_trans_id: str) -> Message | None:
        if not (original_transaction := self.trans_queue.get_transaction(trans_id=original_trans_id)):
            error(f"Lost transaction with ID {original_trans_id}, Cannot build the reversal")
            return

        if not original_transaction.response:
            error(f"Lost response for transaction {original_transaction.trans_id}. Cannot build the reversal")
            return

        reversal_trans_id = original_transaction.trans_id + "_R"
        existed_reversal = self.trans_queue.get_transaction(reversal_trans_id)

        if existed_reversal:
            self.trans_queue.remove_from_queue(existed_reversal)
            message = Message(transaction=existed_reversal.request.transaction)
            return message

        fields = original_transaction.request.transaction.fields.copy()

        for field in self.spec.get_reversal_fields():
            fields[field] = original_transaction.response.transaction.fields.get(field)

        if self.config.fields.build_fld_90:
            fields[self.spec.FIELD_SET.FIELD_090_ORIGINAL_DATA_ELEMENTS] = \
                self.generator.generate_original_data_elements(original_transaction.request)

        reversal_mti = self.spec.get_reversal_mti(original_transaction.request.transaction.message_type)
        reversal = Message(transaction=TransactionModel(message_type=reversal_mti, fields=fields))
        reversal.transaction.original_id = original_transaction.trans_id
        reversal.transaction.id = reversal_trans_id
        reversal.config.generate_fields = list()
        return reversal
