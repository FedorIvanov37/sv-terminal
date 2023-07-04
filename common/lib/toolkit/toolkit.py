from common.lib.core.EpaySpecification import EpaySpecification, IsoField


spec: EpaySpecification = EpaySpecification()


def mask_secret(value: str) -> str:
    return '#' * len(value)


def mask_pan(pan: str):
    pan_spec: IsoField = spec.get_field_spec([spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER])
    length = len(pan)

    if length < pan_spec.min_length or length > pan_spec.max_length or not pan.isdigit():
        return pan

    head: int = 6
    tail: int = 4
    hide: int = length - head - tail
    head: str = pan[:head]
    tail: str = pan[-tail:]
    hide: str = '#' * hide

    return f"{head}{hide}{tail}"
