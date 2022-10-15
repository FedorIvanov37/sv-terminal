from PyQt5.Qt import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtNetwork import QTcpSocket
# from PyQt5.QtWidgets import QPushButton
from json import dumps
from logging import error, info, debug
from typing import Optional
from common.app.core.windows.main_window import MainWindow
from common.app.core.windows.reversal_window import ReversalWindow
from common.app.core.windows.settings_window import SettingsWindow
from common.app.core.windows.spec_window import SpecWindow
from common.app.core.tools.parser import Parser
from common.app.core.tools.logger import Logger
from common.app.core.tools.transaction_queue import TransactionQueue
from common.app.data_models.config import Config
from common.app.core.tools.transaction import Transaction
from common.app.constants.DataFormats import DataFormats
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.constants.TextConstants import TextConstants
from common.app.data_models.message import Message
from common.app.data_models.message import TransactionModel
from common.app.core.tools.connector import ConnectionWorker
from common.app.core.tools.fields_generator import FieldsGenerator
from common.app.core.tools.api.api import TerminalApi


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

        # Working with connection thread
        self._connection_thread: QThread = QThread()
        self.connector = ConnectionWorker(self.config)
        self.connector.moveToThread(self._connection_thread)
        self._need_reconnect.connect(self.connector.connect_sv)
        self._send_message.connect(self.connector.send_message)
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

        if self.config.terminal.run_api:
            self.run_http_server()
            self.window.set_api_status(state=True)

        self.logger.print_config(level=debug)
        info("Startup finished")

    def socket_error(self):
        if self.connector.error() == -1:  # TODO
            return
        
        error("Received socket error: %s", self.connector.error_string())

    def send(self, message: Message) -> None:
        if self.config.debug.clear_log:
            self.window.clear_log()

        message.transaction.id = self.generator.trans_id()

        for field in message.transaction.fields:
            if field not in message.config.generate_fields:
                continue

            field_data = self.generator.generate_field(field)
            message.transaction.fields[field] = field_data

            if self.sender() is self.window.button_send:
                self.window.set_field_value(field, field_data)

        if self.config.fields.send_internal_id:  # TODO
            try:
                message.transaction.fields["47"]["072"] = message.transaction.id
            except (KeyError, TypeError):
                ...

        for string in self.parser.create_sv_dump(message).split("\n"):
            debug(string)

        try:
            transaction: Transaction = self.trans_queue.create_transaction(request=message)
        except ConnectionError:
            return

        info("Processing transaction with internal ID [%s]", transaction.trans_id)

        self.logger.print_message(message)
        self._send_message.emit(message)
        transaction.start_timer()

    def settings(self):
        SettingsWindow(self.config).exec_()

    def specification(self):
        spec_window: SpecWindow = SpecWindow(self.window)
        spec_window.spec_accepted.connect(lambda: info("Specification accepted"))
        spec_window.exec_()

    def get_reversal_id(self):
        transaction_list: list[Transaction] = self.trans_queue.get_reversible_transactions()
        return ReversalWindow.get_reversal_id(transaction_list)

    def save_message_to_file(self, filename: str, message: Message, file_format: str) -> None:
        file_data = None

        if file_format not in DataFormats.get_output_file_formats():
            error("Wrong output file format")
            return

        match file_format:

            case DataFormats.JSON:
                file_data = dumps(message.dict(), indent=4)

            case DataFormats.INI:
                file_data = self.parser.message_to_ini_string(message)

            case DataFormats.DUMP:
                file_data = self.parser.create_sv_dump(message)
                file_data = file_data[1:]

        if file_data is not None:
            with open(filename, "w") as file:
                file.write(file_data)

            info(f"The message was saved successfully to {filename}")

            return

        error("File writing error")

    def disconnect(self):
        self.connector.disconnect_sv()

    def reconnect(self):
        info("[Re]connecting...")
        self._need_reconnect.emit()

    def read_from_socket(self):
        data = self.connector.read_from_socket().data()

        try:
            message: Message = self.parser.parse_dump(data=data)
        except Exception as e:
            error("Incoming message parsing error: %s", e)
            return

        self.trans_queue.put_response(message)

        for string in self.parser.create_sv_dump(message).split("\n"):
            debug(string)

        self.logger.print_message(message)

    def print_data(self, data_format: str) -> None:
        if data_format not in DataFormats.get_print_data_formats():
            error("Wrong format of output data: %s", data_format)
            return

        message: Message = self.parser.parse_form(self.window)

        if message is None:
            error("MainWindow parsing error")
            return

        match data_format:
            case DataFormats.JSON:
                text = dumps(message.dict(), indent=4)

            case DataFormats.DUMP:
                text = self.parser.create_sv_dump(message)

            case DataFormats.INI:
                text = self.parser.message_to_ini_string(message)

            case DataFormats.SPEC:
                text = dumps(self.spec.spec.dict(), indent=4)

            case DataFormats.SV_TERMINAL:
                text = TextConstants.HELLO_MESSAGE

            case _:
                error("Incorrect data format")
                return

        self.window.log_browser.setText(text)

    @staticmethod
    def set_clipboard_text(data: str) -> None:
        QApplication.clipboard().setText(data)

    def reverse(self, trans_id: str | None = None) -> None:
        try:
            trans = self.trans_queue.get_transaction(trans_id=trans_id, reversible=True)
        except ValueError:
            error("Transaction queue has no reversible transactions. Cannot build the reversal")
            return

        if trans is None:
            error("The transaction with id %s wasn't found or has non-reversible MTI", trans_id)
            return

        reversal = self.build_reversal(trans)

        if reversal is None:
            return

        self.send(reversal)

    def build_reversal(self, transaction: Transaction) -> Optional[Message]:
        if not transaction.response:
            error("Lost response for transaction %s. Cannot build the reversal", transaction.trans_id)
            return

        reversal_trans_id = transaction.trans_id + "_R"
        existed_reversal = self.trans_queue.get_transaction(reversal_trans_id)

        if existed_reversal:
            self.trans_queue.remove_from_queue(existed_reversal)
            return Message(transaction=existed_reversal.request.transaction)

        fields = transaction.request.transaction.fields.copy()

        for field in self.spec.get_reversal_fields():
            fields[field] = transaction.response.transaction.fields.get(field)

        if self.config.fields.build_fld_90:
            fields[self.spec.FIELD_SET.FIELD_090_ORIGINAL_DATA_ELEMENTS] = \
                self.generator.generate_original_data_elements(transaction.request)

        reversal_mti = self.spec.get_reversal_mti(transaction.request.transaction.message_type_indicator)
        reversal = Message(transaction=TransactionModel(message_type_indicator=reversal_mti, fields=fields))
        reversal.transaction.original_id = transaction.trans_id
        reversal.transaction.id = transaction.trans_id + "_R"
        reversal.config.generate_fields = list()
        return reversal
