from typing import Final
from enum import StrEnum
from logging import _levelToName as Levels


class DebugLevels(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    NOTSET = "NOTSET"


DISPLAY_DATE_FORMAT: Final[str] = "%T"
LOGFILE_DATE_FORMAT: Final[str] = "%d.%m.%Y %T"

FORMAT: Final[str] = "{asctime} [{levelname}] {message}"
MARK_STYLE: Final[str] = "{"
LOG_MAX_SIZE_MEGABYTES: Final[int] = 10
BACKUP_COUNT: Final[int] = 10
RAISE_EXCEPTIONS: bool = False

LOG_LEVEL: Final[list[str]] = list(Levels.values())

for unused_level in DebugLevels.CRITICAL, DebugLevels.NOTSET:
    LOG_LEVEL.remove(unused_level)
