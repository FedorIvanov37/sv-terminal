from logging import _levelToName as levels
from dataclasses import dataclass


@dataclass
class LogDefinition:
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    NOTSET = "NOTSET"

    DATE_FORMAT = "%T"
    FORMAT = "{asctime} [{levelname}] {message}"
    MARK_STYLE = "{"
    LOG_MAX_SIZE_MEGABYTES = 10
    BACKUP_COUNT = 10

    LOG_LEVEL = list(levels.values())
    LOG_LEVEL.remove(CRITICAL)
    LOG_LEVEL.remove(NOTSET)
