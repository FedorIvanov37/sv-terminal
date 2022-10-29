from datetime import datetime
from random import randint


def trans_id():
    return f"{datetime.now():%Y%m%d_%H%M%S_%f}{randint(0, 999):03}"
