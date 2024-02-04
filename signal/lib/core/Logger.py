from logging import debug, getLevelName, getLogger, Formatter
from logging.handlers import RotatingFileHandler
from signal.lib.constants import LogDefinition
from signal.lib.core.EpaySpecification import EpaySpecification
from signal.lib.data_models.Config import Config
from signal.lib.enums.TermFilesPath import TermFilesPath


class LogStream:
    def __init__(self, log_browser):
        self.log_browser = log_browser

    def write(self, data):
        self.log_browser.append(data)

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

    def __init__(self, config: Config):
        self.config: Config = config
        self.setup()

    def setup(self):
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

        debug("Logger started")
