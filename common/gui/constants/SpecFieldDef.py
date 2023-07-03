from enum import Enum
from dataclasses import dataclass


@dataclass
class SpecFieldDefinition:

    class _Columns(Enum):
        FIELD: str = "Field"
        DESCRIPTION: str = "Description"
        MIN_LENGTH: str = "Min Len"
        MAX_LENGTH: str = "Max Len"
        VARIABLE_LENGTH: str = "Data Len"
        TAG_LENGTH: str = "Tag Len"
        ALPHA: str = "Alpha"
        NUMERIC: str = "Numeric"
        SPECIAL: str = "Special"
        USE_FOR_MATCHING: str = "Matching"
        USE_FOR_REVERSAL: str = "Reversal"
        CAN_BE_GENERATED: str = "Generated"

    @dataclass
    class ColumnsOrder:
        FIELD = 0
        DESCRIPTION = 1
        MIN_LENGTH = 2
        MAX_LENGTH = 3
        VARIABLE_LENGTH = 4
        TAG_LENGTH = 5
        ALPHA = 6
        NUMERIC = 7
        SPECIAL = 8
        USE_FOR_MATCHING = 9
        USE_FOR_REVERSAL = 10
        CAN_BE_GENERATED = 11

    COLUMNS = (column.value for column in _Columns)

    CHECKBOXES = (
            ColumnsOrder.USE_FOR_MATCHING,
            ColumnsOrder.USE_FOR_REVERSAL,
            ColumnsOrder.CAN_BE_GENERATED,
            ColumnsOrder.ALPHA,
            ColumnsOrder.NUMERIC,
            ColumnsOrder.SPECIAL
    )
