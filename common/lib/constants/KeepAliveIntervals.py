TRANS_TYPE_TRANSACTION = "Transaction"
TRANS_TYPE_KEEP_ALIVE = "Keep Alive"

KEEP_ALIVE_1S = "1 second"
KEEP_ALIVE_5S = "5 seconds"
KEEP_ALIVE_10S = "10 seconds"
KEEP_ALIVE_30S = "30 seconds"
KEEP_ALIVE_60S = "60 seconds"
KEEP_ALIVE_300S = "300 seconds"
KEEP_ALIVE_DEFAULT = "%s second(s)"
KEEP_ALIVE_ONCE = "Send once"
KEEP_ALIVE_STOP = "Stop"


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
