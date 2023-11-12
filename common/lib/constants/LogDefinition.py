from typing import Final
from logging import _levelToName as Levels
from logging import debug, info, warning, error, critical


DEBUG: Final[str] = "DEBUG"
INFO: Final[str] = "INFO"
WARNING: Final[str] = "WARNING"
ERROR: Final[str] = "ERROR"
CRITICAL: Final[str] = "CRITICAL"
NOTSET: Final[str] = "NOTSET"

DISPLAY_DATE_FORMAT: Final[str] = "%T"
LOGFILE_DATE_FORMAT: Final[str] = "%d.%m.%Y %H:%M:%S"

FORMAT: Final[str] = "{asctime} [{levelname}] {message}"
MARK_STYLE: Final[str] = "{"
LOG_MAX_SIZE_MEGABYTES: Final[int] = 10
BACKUP_COUNT: Final[int] = 10

LOG_LEVEL: Final[list[str]] = list(Levels.values())
LOG_LEVEL.remove(CRITICAL)
LOG_LEVEL.remove(NOTSET)


def get_level_by_name(level_name, default=True):
    levels_map = {
        DEBUG: debug,
        INFO: info,
        ERROR: error,
        WARNING: warning,
        CRITICAL: critical,
    }

    if not (level := levels_map.get(level_name)):
        if not default:
            raise LookupError(f"Lost debug level {level_name}")

        return info

    return level
