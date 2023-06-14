class SpecFieldDef(object):
    FIELD: str = "Field"
    DESCRIPTION: str = "Description"
    MIN_LENGTH: str = "Min Len"
    MAX_LENGTH: str = "Max Len"
    VARIABLE_LENGTH: str = "Data Len"
    TAG_LENGTH: str = "Tag Len"
    USE_FOR_MATCHING: str = "Matching"
    USE_FOR_REVERSAL: str = "Reversal"
    CAN_BE_GENERATED: str = "Generated"
    ALPHA: str = "Alpha"
    NUMERIC: str = "Numeric"
    SPECIAL: str = "Special"

    COLUMNS: tuple[str, str, str, str, str, str, str, str, str, str, str, str, str, str, str] = (
        FIELD,
        DESCRIPTION,
        MIN_LENGTH,
        MAX_LENGTH,
        VARIABLE_LENGTH,
        TAG_LENGTH,
        ALPHA,
        NUMERIC,
        SPECIAL,
        # BYTES,
        USE_FOR_MATCHING,
        USE_FOR_REVERSAL,
        CAN_BE_GENERATED,
        # IS_SECRET,
    )

    CHECKBOXES: tuple[str, str, str, str, str, str, str, str] = (
        USE_FOR_MATCHING,
        USE_FOR_REVERSAL,
        CAN_BE_GENERATED,
        ALPHA,
        NUMERIC,
        SPECIAL,
        # BYTES,
        # IS_SECRET
    )

    @staticmethod
    def get_column_position(column):
        return SpecFieldDef.COLUMNS.index(column)

    @staticmethod
    def get_checkbox_positions():
        pos = []

        for column in SpecFieldDef.COLUMNS:
            if column in SpecFieldDef.CHECKBOXES:
                pos.append(SpecFieldDef.COLUMNS.index(column))

        return pos
