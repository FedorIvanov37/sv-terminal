from logging import info, debug, getLevelName, getLogger, Formatter
from logging.handlers import RotatingFileHandler
from json import dumps
from common.app.constants.LogDefinition import LogDefinition
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.core.tools.wireless_log_handler import WirelessHandler
from common.app.core.tools.parser import Parser
from common.app.data_models.message import Message
from common.app.core.tools.bitmap import Bitmap
from common.app.data_models.config import Config
from common.app.constants.FilePath import FilePath


class Logger:
    class LogStream:
        def __init__(self, log_browser):
            self.log_browser = log_browser

        def write(self, data):
            self.log_browser.append(data)

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

    def __init__(self, stream, config: Config):
        self.output = stream
        self.config: Config = config
        self.parser: Parser = Parser(self.config)
        self.setup()

    def setup(self):
        logger = getLogger()
        logger.handlers.clear()
        logger.setLevel(getLevelName(self.config.debug.level))
        formatter = Formatter(LogDefinition.FORMAT, LogDefinition.DATE_FORMAT, LogDefinition.MARK_STYLE)
        wireless_handler = WirelessHandler()
        stream = Logger.LogStream(self.output)
        wireless_handler.new_record_appeared.connect(lambda record: stream.write(data=record))
        file_handler = RotatingFileHandler(
            filename=FilePath.LOG_FILE_NAME,
            maxBytes=LogDefinition.LOG_MAX_SIZE_MEGABYTES * 1024000,
            backupCount=LogDefinition.BACKUP_COUNT
        )

        for handler in (wireless_handler, file_handler):
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        debug("Logger started")

    def print_config(self, config=None, level=_default_level):
        level("### Configuration Parameters ###")

        if config is None:
            config = self.config

        level(dumps(config.dict(), indent=4))

    def print_message(self, message: Message, level=_default_level) -> None:
        def put(string, size=0):
            return (f" [%{size}s]" % string).strip()

        bitmap = Bitmap(message.transaction.fields)

        level("")

        if message.transaction.id:
            level("[TRANS ID][%s]", message.transaction.id)

        if message.transaction.utrnno:
            level("[UTRNNO  ][%s]", message.transaction.utrnno)

        level("[MSG TYPE][%s]", message.transaction.message_type_indicator)
        level("[BITMAP  ][%s]", bitmap.get_bitmap(str))

        for field, field_data in message.transaction.fields.items():
            if field == self.spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY:
                continue

            log_set = str()
            log_set += put(str(field).zfill(3))

            if isinstance(field_data, dict):
                field_data = self.parser.join_complex_field(field, field_data)

            log_set += put(str(len(field_data)).zfill(3))
            log_set += put(field_data)
            log_set = log_set.strip()

            level(log_set)

        level("")
