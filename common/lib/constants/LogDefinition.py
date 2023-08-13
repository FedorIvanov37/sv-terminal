from dataclasses import dataclass
from logging import _levelToName as Levels
from logging import debug, info, warning, error, critical


@dataclass(frozen=True)
class LogDefinition(object):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    NOTSET = "NOTSET"

    DISPLAY_DATE_FORMAT = "%T"
    LOGFILE_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"

    FORMAT = "{asctime} [{levelname}] {message}"
    MARK_STYLE = "{"
    LOG_MAX_SIZE_MEGABYTES = 10
    BACKUP_COUNT = 10

    LOG_LEVEL = list(Levels.values())
    LOG_LEVEL.remove(CRITICAL)
    LOG_LEVEL.remove(NOTSET)

    @staticmethod
    def get_level_by_name(level_name, default=True):
        levels_map = {
            LogDefinition.DEBUG: debug,
            LogDefinition.INFO: info,
            LogDefinition.ERROR: error,
            LogDefinition.WARNING: warning,
            LogDefinition.CRITICAL: critical,
        }

        if not (level := levels_map.get(level_name)):
            if not default:
                raise LookupError(f"Lost debug level {level_name}")
            
            return info

        return level
