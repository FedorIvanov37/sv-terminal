from logging import info, debug, getLevelName, getLogger, Formatter
from logging.handlers import RotatingFileHandler
from json import dumps
from common.gui.constants.LogDefinition import LogDefinition
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.core.Parser import Parser
from common.lib.data_models.Config import Config
from common.lib.data_models.Transaction import Transaction
from common.gui.constants.TermFilesPath import TermFilesPath


class LogStream:
    def __init__(self, log_browser):
        self.log_browser = log_browser

    def write(self, data):
        self.log_browser.append(data)


class Logger:
    _spec = EpaySpecification()
    _default_level = info
    _stream = None

    @property
    def spec(self):
        return self._spec

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, stream):
        self._stream = stream

    def __init__(self, config: Config):
        self.config: Config = config
        self.parser: Parser = Parser(self.config)
        self.setup()

    def setup(self):
        logger = getLogger()
        logger.handlers.clear()
        logger.setLevel(getLevelName(self.config.debug.level))
        formatter = Formatter(LogDefinition.FORMAT, LogDefinition.DATE_FORMAT, LogDefinition.MARK_STYLE)
        file_handler = RotatingFileHandler(
            filename=TermFilesPath.LOG_FILE_NAME,
            maxBytes=LogDefinition.LOG_MAX_SIZE_MEGABYTES * 1024000,
            backupCount=LogDefinition.BACKUP_COUNT
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        debug("Logger started")

    def print_dump(self, transaction: Transaction):
        for string in self.parser.create_sv_dump(transaction).split("\n"):
            debug(string)

    def print_config(self, config=None, level=_default_level):
        level("### Configuration Parameters ###")

        if config is None:
            config = self.config

        level(dumps(config.dict(), indent=4))

    def print_transaction(self, transaction: Transaction, level=_default_level) -> None:
        def put(string: str, size=0):
            return f"[{string.zfill(size)}]"

        level("")

        # bitmap: str = Bitmap(transaction.data_fields).get_bitmap(str)

        bitmap = ", ".join(transaction.data_fields.keys())

        trans_id = transaction.trans_id

        if transaction.matched and not transaction.is_request:
            trans_id = transaction.match_id

        level(f"[TRANS_ID][{trans_id}]")

        if transaction.utrnno:
            level(f"[UTRNNO  ][{transaction.utrnno}]")

        level(f"[MSG_TYPE][{transaction.message_type}]")
        level(f"[BITMAP  ][{bitmap}]")

        for field, field_data in transaction.data_fields.items():
            if field == self.spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY:
                continue

            log_set = str()
            log_set += put(field, size=3)

            if isinstance(field_data, dict):
                field_data = self.parser.join_complex_field(field, field_data)

            length = str(len(field_data))
            log_set += put(length, size=3)
            log_set += put(field_data)
            log_set = log_set.strip()

            level(log_set)

        level("")
