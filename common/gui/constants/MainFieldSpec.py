from common.lib.core.EpaySpecification import EpaySpecification


class MainFieldSpec(object):
    spec: EpaySpecification = EpaySpecification()
    FIELD: str = "Field"
    VALUE: str = "Value"
    LENGTH: str = "Length"
    DESCRIPTION: str = "Description"
    PROPERTY: str = "Property"
    GENERATE: str = "Generate"

    columns: tuple[str, str, str, str, str] = (FIELD, VALUE, LENGTH, DESCRIPTION, PROPERTY)

    columns_order: dict[str, int] = {
        FIELD: 0,
        VALUE: 1,
        LENGTH: 2,
        DESCRIPTION: 3,
        PROPERTY: 4
    }

    generated_fields: list[str] = [
        spec.FIELD_SET.FIELD_004_TRANSACTION_AMOUNT,
        spec.FIELD_SET.FIELD_007_TRANSMISSION_DATE_AND_TIME,
        spec.FIELD_SET.FIELD_011_SYSTEM_TRACE_AUDIT_NUMBER,
        spec.FIELD_SET.FIELD_012_TRANSACTION_LOCAL_DATE_AND_TIME,
        spec.FIELD_SET.FIELD_037_RETRIEVAL_REFERENCE_NUMBER
    ]
