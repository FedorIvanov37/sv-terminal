from typing import Final
from enum import Enum


class _Columns(Enum):
    FIELD: Final[str] = "Field"
    DESCRIPTION: Final[str] = "Description"
    MIN_LENGTH: Final[str] = "Min Len"
    MAX_LENGTH: Final[str] = "Max Len"
    VARIABLE_LENGTH: Final[str] = "Data Len"
    TAG_LENGTH: Final[str] = "Tag Len"
    ALPHA: Final[str] = "Alpha"
    NUMERIC: Final[str] = "Numeric"
    SPECIAL: Final[str] = "Special"
    USE_FOR_MATCHING: Final[str] = "Matching"
    USE_FOR_REVERSAL: Final[str] = "Reversal"
    CAN_BE_GENERATED: Final[str] = "Generated"
    SECRET: Final[str] = "Secret"


class ColumnsOrder:
    FIELD: Final[int] = 0
    DESCRIPTION: Final[int] = 1
    MIN_LENGTH: Final[int] = 2
    MAX_LENGTH: Final[int] = 3
    VARIABLE_LENGTH: Final[int] = 4
    TAG_LENGTH: Final[int] = 5
    ALPHA: Final[int] = 6
    NUMERIC: Final[int] = 7
    SPECIAL: Final[int] = 8
    USE_FOR_MATCHING: Final[int] = 9
    USE_FOR_REVERSAL: Final[int] = 10
    CAN_BE_GENERATED: Final[int] = 11
    SECRET: Final[int] = 12


COLUMNS = tuple(column.value for column in _Columns)


CHECKBOXES = (
    ColumnsOrder.USE_FOR_MATCHING,
    ColumnsOrder.USE_FOR_REVERSAL,
    ColumnsOrder.CAN_BE_GENERATED,
    ColumnsOrder.ALPHA,
    ColumnsOrder.NUMERIC,
    ColumnsOrder.SPECIAL,
    ColumnsOrder.SECRET,
)


SPECIFICATION: Final[str] = "Specification"
