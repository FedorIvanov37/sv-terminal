from enum import StrEnum, IntEnum


class Columns(StrEnum):
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


ColumnsOrder = IntEnum(
    "ColumnsOrder", {column: position for position, column in enumerate([column.name for column in Columns])}
)


checkboxes_list = (
    ColumnsOrder.USE_FOR_MATCHING,
    ColumnsOrder.USE_FOR_REVERSAL,
    ColumnsOrder.CAN_BE_GENERATED,
    ColumnsOrder.ALPHA,
    ColumnsOrder.NUMERIC,
    ColumnsOrder.SPECIAL,
    ColumnsOrder.SECRET
)


Checkboxes = IntEnum(
    "Checkboxes", {column.name: column.value for column in checkboxes_list}
)
