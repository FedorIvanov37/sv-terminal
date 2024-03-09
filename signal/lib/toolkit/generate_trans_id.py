from datetime import datetime
from random import randint


def generate_trans_id() -> str:
    return f"{datetime.now():%Y%m%d_%H%M%S_%f}{randint(1000, 9999)}"
