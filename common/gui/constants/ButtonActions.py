from dataclasses import dataclass


@dataclass
class ButtonAction(object):
    LAST = "Last"
    OTHER = "Other"
    #
    BUTTON_PLUS_SIGN = "✚"
    BUTTON_MINUS_SIGN = "━"
    BUTTON_NEXT_LEVEL_SIGN = "🡾"
    #
    KEEP_ALIVE_1S = "1 second"
    KEEP_ALIVE_5S = "5 seconds"
    KEEP_ALIVE_10S = "10 seconds"
    KEEP_ALIVE_30S = "30 seconds"
    KEEP_ALIVE_60S = "60 seconds"
    KEEP_ALIVE_300S = "300 seconds"
    KEEP_ALIVE_DEFAULT = "%s second(s)"
    KEEP_ALIVE_ONCE = "Send once"
    KEEP_ALIVE_STOP = "Stop"
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
    def get_interval_time(interval_name):
        interval_map = {
            ButtonAction.KEEP_ALIVE_1S: 1,
            ButtonAction.KEEP_ALIVE_5S: 5,
            ButtonAction.KEEP_ALIVE_10S: 10,
            ButtonAction.KEEP_ALIVE_30S: 30,
            ButtonAction.KEEP_ALIVE_60S: 60,
            ButtonAction.KEEP_ALIVE_300S: 300,
        }

        return interval_map.get(interval_name, None)

    @staticmethod
    def get_reversal_actions():
        return ButtonAction.LAST, ButtonAction.OTHER
