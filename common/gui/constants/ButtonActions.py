from dataclasses import dataclass
from common.lib.constants.KeepAliveIntervals import KeepAliveInterval


@dataclass
class ButtonAction(object):
    LAST = "Last"
    OTHER = "Other"
    #
    ONE_SESSION = "For current session"
    PERMANENTLY = "Permanently"
    #
    BUTTON_PLUS_SIGN = "✚"
    BUTTON_MINUS_SIGN = "━"
    BUTTON_NEXT_LEVEL_SIGN = "🡾"
    #
    KEEP_ALIVE_1S = KeepAliveInterval.KEEP_ALIVE_1S
    KEEP_ALIVE_5S = KeepAliveInterval.KEEP_ALIVE_5S
    KEEP_ALIVE_10S = KeepAliveInterval.KEEP_ALIVE_10S
    KEEP_ALIVE_30S = KeepAliveInterval.KEEP_ALIVE_30S
    KEEP_ALIVE_60S = KeepAliveInterval.KEEP_ALIVE_60S
    KEEP_ALIVE_300S = KeepAliveInterval.KEEP_ALIVE_300S
    KEEP_ALIVE_DEFAULT = KeepAliveInterval.KEEP_ALIVE_DEFAULT
    KEEP_ALIVE_ONCE = KeepAliveInterval.KEEP_ALIVE_ONCE
    KEEP_ALIVE_STOP = KeepAliveInterval.KEEP_ALIVE_STOP
    #
    CURRENT_ACTION_MARK = "•"

    @staticmethod
    def get_interval_names():
        return [
            ButtonAction.KEEP_ALIVE_1S,
            ButtonAction.KEEP_ALIVE_5S,
            ButtonAction.KEEP_ALIVE_10S,
            ButtonAction.KEEP_ALIVE_30S,
            ButtonAction.KEEP_ALIVE_60S,
            ButtonAction.KEEP_ALIVE_300S,
            ButtonAction.KEEP_ALIVE_ONCE,
            ButtonAction.KEEP_ALIVE_STOP,
        ]

    @staticmethod
    def get_reversal_actions():
        return ButtonAction.LAST, ButtonAction.OTHER
