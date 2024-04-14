import logging
from logging import debug, getLevelName, getLogger, Formatter, StreamHandler, info
from common.gui.core.WirelessHandler import WirelessHandler
from logging.handlers import RotatingFileHandler
from common.lib.constants import LogDefinition
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.Config import Config
from common.lib.enums.TermFilesPath import TermFilesPath
from common.lib.decorators.singleton import singleton


class LogStream:
    def __init__(self, log_browser):
        self.log_browser = log_browser

    def write(self, data):
        self.log_browser.append(data)


@singleton
class Logger:
    _spec = EpaySpecification()
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

    def __init__(self, config: Config, display_log=False):
        self.config: Config = config
        self.setup(display_log=display_log)

    def setup(self, display_log=False):
        logger = getLogger()
        logger.handlers.clear()
        logger.setLevel(getLevelName(self.config.debug.level))

        formatter = Formatter(LogDefinition.FORMAT, LogDefinition.LOGFILE_DATE_FORMAT, LogDefinition.MARK_STYLE)

        file_handler = RotatingFileHandler(
            filename=TermFilesPath.LOG_FILE_NAME,
            maxBytes=LogDefinition.LOG_MAX_SIZE_MEGABYTES * 1024000,
            backupCount=self.config.debug.backup_storage_depth,
            encoding='utf8'
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if display_log:
            stream_handler = StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        logging.raiseExceptions = LogDefinition.RAISE_EXCEPTIONS

        debug("Logger started")

    def set_debug_level(self, level=None):
        if level is None:
            level = self.config.debug.level

        if not level:
            return

        getLogger().setLevel(getLevelName(level))

    @staticmethod
    def create_window_logger(log_browser, formatter: Formatter | None = None) -> WirelessHandler:
        if formatter is None:
            formatter: Formatter = Formatter(
                LogDefinition.FORMAT,
                LogDefinition.DISPLAY_DATE_FORMAT,
                LogDefinition.MARK_STYLE
            )

        stream: LogStream = LogStream(log_browser)
        wireless_handler = WirelessHandler()
        wireless_handler.new_record_appeared.connect(lambda record: stream.write(data=record))
        wireless_handler.setFormatter(formatter)
        logger = getLogger()
        logger.addHandler(wireless_handler)

        return wireless_handler

    @staticmethod
    def create_logger():
        formatter: Formatter = Formatter(LogDefinition.FORMAT, LogDefinition.DISPLAY_DATE_FORMAT, LogDefinition.MARK_STYLE)
        logger = getLogger()
        handler = StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
