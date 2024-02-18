from typing import Final
from enum import StrEnum
from logging import _levelToName as Levels
from logging import debug, info, warning, error, critical


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

LOG_LEVEL: Final[list[str]] = list(Levels.values())

for unused_level in DebugLevels.CRITICAL, DebugLevels.NOTSET:
    LOG_LEVEL.remove(unused_level)


def get_level_by_name(level_name, default=True):
    try:
        DebugLevels[level_name]

    except KeyError:
        if not default:
            raise LookupError(f"Lost debug level {level_name}")

        return info

    levels_map = {
        DebugLevels.DEBUG: debug,
        DebugLevels.INFO: info,
        DebugLevels.ERROR: error,
        DebugLevels.WARNING: warning,
        DebugLevels.CRITICAL: critical,
    }

    try:
        level = levels_map[level_name]
    except KeyError:
        level = info

    return level
