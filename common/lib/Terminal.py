from json import dumps
from logging import error, info, warning
from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, QObject
from common.lib.Parser import Parser
from common.app.core.tools.logger import Logger
from common.lib.TransactionQueue import TransactionQueue
from common.lib.EpaySpecification import EpaySpecification
from common.lib.FieldsGenerator import FieldsGenerator
from common.lib.Validator import Validator
from common.app.constants.DataFormats import DataFormats
from common.app.constants.FilePath import FilePath
from common.lib.data_models.Config import Config
from common.lib.data_models.Transaction import Transaction
from common.app.core.tools.connection_worker import ConnectionWorker


class SvTerminal(QObject):
    _config: Config = Config.parse_file(FilePath.CONFIG)
    _pyqt_application = QtWidgets.QApplication([])
    _validator = Validator(_config)
    _spec: EpaySpecification = EpaySpecification(FilePath.CONFIG)
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

    def __init__(self, config: Config):
        super(SvTerminal, self).__init__()
        self._config = config
        self.parser: Parser = Parser(self.config)
        self.generator = FieldsGenerator()
        self.logger: Logger = Logger(self.config)
        self.connector: ConnectionWorker = ConnectionWorker(self.config)
        self.trans_queue: TransactionQueue = TransactionQueue(self.connector)
        self.connector.socker_error.connect(self.socket_error)
        self.connect_interfaces()

    def run(self):
        status = self._pyqt_application.exec()
        exit(status)

    # def setup(self):
    #     if self.config.terminal.connect_on_startup:
    #         self.reconnect()

    def connect_interfaces(self):
        self.connector.connected.connect(lambda: info("SmartVista host connection ESTABLISHED"))
        self.connector.disconnected.connect(lambda: info("SmartVista host DISCONNECTED"))
        self._need_reconnect.connect(self.connector.connect_sv)
        self.trans_queue.incoming_transaction.connect(self.transaction_received)
        self.trans_queue.outgoing_transaction.connect(self.transaction_sent)
        self.trans_queue.transaction_timeout.connect(self.got_timeout)

    @staticmethod
    def got_timeout(transaction, timeout_secs):
        error(f"Transaction [{transaction.trans_id}] timeout after {int(timeout_secs)} seconds of waiting SmartVista")

    def socket_error(self):
        if self.connector.error() == -1:  # TODO
            return

        error(f"Received a socket error from SmartVista host: {self.connector.error_string}")

    def disconnect(self):
        self.connector.disconnect_sv()

    def reconnect(self):
        info("[Re]connecting...")
        self._need_reconnect.emit()

    def send(self, transaction: Transaction | None = None):
        if transaction.generate_fields:
            transaction: Transaction = self.generator.set_generated_fields(transaction)

        if self.config.fields.send_internal_id:
            transaction: Transaction = self.generator.set_trans_id_to_47_072(transaction)

        if self.config.fields.validation:
            try:
                self.validator.validate_transaction(transaction)
            except (ValueError, TypeError) as validation_error:
                error(f"Transaction validation error {validation_error}")
                return

        self.logger.print_transaction(transaction)

        self.trans_queue.put_transaction(transaction)

    def transaction_received(self, response: Transaction):
        self.logger.print_dump(response)
        self.logger.print_transaction(response)

        if response.matched and response.resp_time_seconds:
            info(f"Transaction ID [{response.match_id}] matched, response time seconds: {response.resp_time_seconds}")
            return

        if not response.matched:
            match_fields = [field for field in self.spec.get_match_fields() if field in response.data_fields]
            match_fields = ', '.join(match_fields)
            warning(f"Non-matched Transaction received. Transaction ID [{response.trans_id}]")
            warning(f"Fields {match_fields} from the response don't correspond to any requests in the current session "
                    f"or request was matched before")
            return

        if not response.resp_time_seconds:
            warning(f"Transaction ID [{response.match_id}] received and matched after timeout 60 seconds")
            return

    def transaction_sent(self, request: Transaction):
        self.logger.print_dump(request)
        self.logger.print_transaction(request)
        info(f"Transaction [{request.trans_id}] was sent ")

    def save_transaction(self, transaction: Transaction, file_format: str, file_name) -> None:
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

        with open(file_name, "w") as file:
            file.write(file_data)

        info(f"The transaction was saved successfully to {file_name}")

    def reverse_transaction(self, id_source: str | None = None, original_id: str | None = None):
        if original_id is None:
            if not (original_id := self.trans_queue.get_last_reversible_transaction_id()):
                return

        if not (original := self.trans_queue.get_transaction(original_id)):
            error(f"Wrong Transaction ID {original_id}, cannot generate the reversal")
            return

        try:
            reversal: Transaction = self.build_reversal(original)
        except LookupError as lookup_error:
            error(lookup_error)
            return

        self.send(reversal)

    def build_reversal(self, original_transaction: Transaction) -> Transaction:
        if not (original_transaction.matched and original_transaction.match_id):
            raise LookupError(f"Lost response for transaction {original_transaction.trans_id}. Cannot build reversal")

        reversal_trans_id = original_transaction.trans_id + "_R"
        existed_reversal = self.trans_queue.get_transaction(reversal_trans_id)

        if existed_reversal:
            self.trans_queue.remove_from_queue(existed_reversal)
            transaction: Transaction = Transaction.parse_obj(existed_reversal)
            transaction.matched = None
            transaction.generate_fields = []
            return transaction

        fields = original_transaction.data_fields.copy()

        for field in self.spec.get_reversal_fields():
            fields[field] = original_transaction.data_fields.get(field)

        if self.config.fields.build_fld_90:
            field90 = self.generator.generate_original_data_elements(original_transaction)
            fields[self.spec.FIELD_SET.FIELD_090_ORIGINAL_DATA_ELEMENTS] = field90

        reversal_mti = self.spec.get_reversal_mti(original_transaction.message_type)

        reversal = Transaction(
            message_type=reversal_mti,
            data_fields=fields,
            trans_id=reversal_trans_id,
            generate_fields=list(),
        )

        return reversal

    def echo_test(self):
        transaction: Transaction = self.parser.parse_file(FilePath.ECHO_TEST)
        self.send(transaction)
