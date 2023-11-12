from common.lib.constants import KeepAliveIntervals


BUTTON_PLUS_SIGN = "✚"
BUTTON_MINUS_SIGN = "━"
BUTTON_NEXT_LEVEL_SIGN = "🡾"
BUTTON_UP_SIGN = "🡹"
BUTTON_DOWN_SIGN = "🡻"
BUTTON_LEFT_SIGN = "🡸"
BUTTON_RIGHT_SIGN = "🡺"

ALL = "All"
STRING = "String"
JSON = "JSON"

GET_DATA = f"{BUTTON_RIGHT_SIGN} Get from MainWindow"
SET_DATA = f"{BUTTON_LEFT_SIGN} Set to MainWindow"

LAST = "Reverse last"
OTHER = "Reverse other"
SET_REVERSAL = "Set Reversal fields"

ONE_SESSION = "For current session"
PERMANENTLY = "Permanently"

REMOTE_SPEC = "Set remote specification"
LOCAL_SPEC = "Set local specification"

KEEP_ALIVE_1S = KeepAliveIntervals.KEEP_ALIVE_1S
KEEP_ALIVE_5S = KeepAliveIntervals.KEEP_ALIVE_5S
KEEP_ALIVE_10S = KeepAliveIntervals.KEEP_ALIVE_10S
KEEP_ALIVE_30S = KeepAliveIntervals.KEEP_ALIVE_30S
KEEP_ALIVE_60S = KeepAliveIntervals.KEEP_ALIVE_60S
KEEP_ALIVE_300S = KeepAliveIntervals.KEEP_ALIVE_300S
KEEP_ALIVE_DEFAULT = KeepAliveIntervals.KEEP_ALIVE_DEFAULT
KEEP_ALIVE_ONCE = KeepAliveIntervals.KEEP_ALIVE_ONCE
KEEP_ALIVE_STOP = KeepAliveIntervals.KEEP_ALIVE_STOP

CURRENT_ACTION_MARK = "•"


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
