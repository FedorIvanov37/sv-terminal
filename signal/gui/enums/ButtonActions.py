from enum import StrEnum
from signal.lib.enums import KeepAlive


class ButtonActionSigns(StrEnum):
    BUTTON_PLUS_SIGN = "✚"
    BUTTON_MINUS_SIGN = "━"
    BUTTON_NEXT_LEVEL_SIGN = "🡾"
    BUTTON_UP_SIGN = "🡹"
    BUTTON_DOWN_SIGN = "🡻"
    BUTTON_LEFT_SIGN = "🡸"
    BUTTON_RIGHT_SIGN = "🡺"


class ClearMenuActions(StrEnum):
    ALL = "All"
    STRING = "String"
    JSON = "JSON"


class DataMenuActions(StrEnum):
    GET_DATA = f"{ButtonActionSigns.BUTTON_RIGHT_SIGN} Get from MainWindow"
    SET_DATA = f"{ButtonActionSigns.BUTTON_LEFT_SIGN} Set to MainWindow"


class ReversalMenuActions(StrEnum):
    LAST = "Reverse last"
    OTHER = "Reverse other"
    SET_REVERSAL = "Set Reversal fields"


class ApplySpecMenuActions(StrEnum):
    ONE_SESSION = "For current session"
    PERMANENTLY = "Permanently"


class SetSpecMenuActions(StrEnum):
    REMOTE_SPEC = "Set remote specification"
    LOCAL_SPEC = "Set local specification"


class KeepAliveTimeIntervals(StrEnum):
    KEEP_ALIVE_1S = KeepAlive.IntervalNames.KEEP_ALIVE_1S
    KEEP_ALIVE_5S = KeepAlive.IntervalNames.KEEP_ALIVE_5S
    KEEP_ALIVE_10S = KeepAlive.IntervalNames.KEEP_ALIVE_10S
    KEEP_ALIVE_30S = KeepAlive.IntervalNames.KEEP_ALIVE_30S
    KEEP_ALIVE_60S = KeepAlive.IntervalNames.KEEP_ALIVE_60S
    KEEP_ALIVE_300S = KeepAlive.IntervalNames.KEEP_ALIVE_300S
    KEEP_ALIVE_DEFAULT = KeepAlive.IntervalNames.KEEP_ALIVE_DEFAULT
    KEEP_ALIVE_ONCE = KeepAlive.IntervalNames.KEEP_ALIVE_ONCE
    KEEP_ALIVE_STOP = KeepAlive.IntervalNames.KEEP_ALIVE_STOP


class Marks(StrEnum):
    CURRENT_ACTION_MARK = "•"
