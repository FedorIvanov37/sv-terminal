from typing import Final


TRANS_TYPE_TRANSACTION: Final[str] = "Transaction"
TRANS_TYPE_KEEP_ALIVE: Final[str] = "Keep Alive"

KEEP_ALIVE_1S: Final[str] = "1 second"
KEEP_ALIVE_5S: Final[str] = "5 seconds"
KEEP_ALIVE_10S: Final[str] = "10 seconds"
KEEP_ALIVE_30S: Final[str] = "30 seconds"
KEEP_ALIVE_60S: Final[str] = "60 seconds"
KEEP_ALIVE_300S: Final[str] = "300 seconds"
KEEP_ALIVE_DEFAULT: Final[str] = "%s second(s)"
KEEP_ALIVE_ONCE: Final[str] = "Send once"
KEEP_ALIVE_STOP: Final[str] = "Stop"


def get_interval_time(interval_name):
    interval_map = {
        KEEP_ALIVE_1S: 1,
        KEEP_ALIVE_5S: 5,
        KEEP_ALIVE_10S: 10,
        KEEP_ALIVE_30S: 30,
        KEEP_ALIVE_60S: 60,
        KEEP_ALIVE_300S: 300,
    }

    return interval_map.get(interval_name, None)
