from typing import Final
from common.lib.constants import KeepAliveIntervals


BUTTON_PLUS_SIGN: Final[str] = "✚"
BUTTON_MINUS_SIGN: Final[str] = "━"
BUTTON_NEXT_LEVEL_SIGN: Final[str] = "🡾"
BUTTON_UP_SIGN: Final[str] = "🡹"
BUTTON_DOWN_SIGN: Final[str] = "🡻"
BUTTON_LEFT_SIGN: Final[str] = "🡸"
BUTTON_RIGHT_SIGN: Final[str] = "🡺"

ALL: Final[str] = "All"
STRING: Final[str] = "String"
JSON: Final[str] = "JSON"

GET_DATA: Final[str] = f"{BUTTON_RIGHT_SIGN} Get from MainWindow"
SET_DATA: Final[str] = f"{BUTTON_LEFT_SIGN} Set to MainWindow"

LAST: Final[str] = "Reverse last"
OTHER: Final[str] = "Reverse other"
SET_REVERSAL: Final[str] = "Set Reversal fields"

ONE_SESSION: Final[str] = "For current session"
PERMANENTLY: Final[str] = "Permanently"

REMOTE_SPEC: Final[str] = "Set remote specification"
LOCAL_SPEC: Final[str] = "Set local specification"

KEEP_ALIVE_1S: Final[str] = KeepAliveIntervals.KEEP_ALIVE_1S
KEEP_ALIVE_5S: Final[str] = KeepAliveIntervals.KEEP_ALIVE_5S
KEEP_ALIVE_10S: Final[str] = KeepAliveIntervals.KEEP_ALIVE_10S
KEEP_ALIVE_30S: Final[str] = KeepAliveIntervals.KEEP_ALIVE_30S
KEEP_ALIVE_60S: Final[str] = KeepAliveIntervals.KEEP_ALIVE_60S
KEEP_ALIVE_300S: Final[str] = KeepAliveIntervals.KEEP_ALIVE_300S
KEEP_ALIVE_DEFAULT: Final[str] = KeepAliveIntervals.KEEP_ALIVE_DEFAULT
KEEP_ALIVE_ONCE: Final[str] = KeepAliveIntervals.KEEP_ALIVE_ONCE
KEEP_ALIVE_STOP: Final[str] = KeepAliveIntervals.KEEP_ALIVE_STOP

CURRENT_ACTION_MARK: Final[str] = "•"


def get_interval_names():
    return [
        KEEP_ALIVE_1S,
        KEEP_ALIVE_5S,
        KEEP_ALIVE_10S,
        KEEP_ALIVE_30S,
        KEEP_ALIVE_60S,
        KEEP_ALIVE_300S,
        KEEP_ALIVE_ONCE,
        KEEP_ALIVE_STOP,
    ]


def get_reversal_actions():
    return LAST, OTHER
