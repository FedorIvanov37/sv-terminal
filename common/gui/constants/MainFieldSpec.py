from typing import Final
from enum import Enum
from common.lib.core.EpaySpecification import EpaySpecification


class ColumnsOrder:
    FIELD: Final[int] = 0
    VALUE: Final[int] = 1
    LENGTH: Final[int] = 2
    DESCRIPTION: Final[int] = 3
    PROPERTY: Final[int] = 4


class Columns(Enum):
    FIELD: Final[str] = "Field"
    VALUE: Final[str] = "Value"
    LENGTH: Final[str] = "Length"
    DESCRIPTION: Final[str] = "Description"
    PROPERTY: Final[str] = "Property"


MESSAGE: Final[str] = "Message"

spec: EpaySpecification = EpaySpecification()

columns = tuple(field.value for field in Columns)

generated_fields = (
    spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT,
    spec.FIELD_SET.FIELD_007_TRANSMISSION_DATE_AND_TIME,
    spec.FIELD_SET.FIELD_011_SYSTEM_TRACE_AUDIT_NUMBER,
    spec.FIELD_SET.FIELD_012_TRANSACTION_LOCAL_DATE_AND_TIME,
    spec.FIELD_SET.FIELD_037_RETRIEVAL_REFERENCE_NUMBER,
)
