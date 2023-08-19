from enum import Enum
from dataclasses import dataclass


@dataclass
class SpecFieldDefinition:
    SPECIFICATION = "Specification"


    class _Columns(Enum):
        FIELD = "Field"
        DESCRIPTION = "Description"
        MIN_LENGTH = "Min Len"
        MAX_LENGTH = "Max Len"
        VARIABLE_LENGTH = "Data Len"
        TAG_LENGTH = "Tag Len"
        ALPHA = "Alpha"
        NUMERIC = "Numeric"
        SPECIAL = "Special"
        USE_FOR_MATCHING = "Matching"
        USE_FOR_REVERSAL = "Reversal"
        CAN_BE_GENERATED = "Generated"
        SECRET = "Secret"


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
        SECRET = 12


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
