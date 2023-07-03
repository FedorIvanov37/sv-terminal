from common.lib.core.EpaySpecification import EpaySpecification
from dataclasses import dataclass
from enum import Enum


@dataclass
class ColumnsOrder:
    FIELD = 0
    VALUE = 1
    LENGTH = 2
    DESCRIPTION = 3
    PROPERTY = 4


class Columns(Enum):
    FIELD = "Field"
    VALUE = "Value"
    LENGTH = "Length"
    DESCRIPTION = "Description"
    PROPERTY = "Property"


class MainFieldSpec(object):
    columns = (field.value for field in Columns)
    spec: EpaySpecification = EpaySpecification()

    generated_fields: list[str] = [
        spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT,
        spec.FIELD_SET.FIELD_007_TRANSMISSION_DATE_AND_TIME,
        spec.FIELD_SET.FIELD_011_SYSTEM_TRACE_AUDIT_NUMBER,
        spec.FIELD_SET.FIELD_012_TRANSACTION_LOCAL_DATE_AND_TIME,
        spec.FIELD_SET.FIELD_037_RETRIEVAL_REFERENCE_NUMBER
    ]
