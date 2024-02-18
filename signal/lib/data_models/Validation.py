from enum import StrEnum
from pydantic import BaseModel


class ValidationTypes(StrEnum):
    FIELD_DATA_PRE_VALIDATION = "FIELD_DATA_PRE_VALIDATION"
    FIELD_DATA_MAIN_VALIDATION = "FIELD_DATA_MAIN_VALIDATION"
    FIELD_DATA_CUSTOM_VALIDATION = "FIELD_DATA_CUSTOM_VALIDATION"
    EXTENDED_VALIDATION = "EXTENDED_VALIDATION"
    TRANSACTION_VALIDATION = "TRANSACTION_VALIDATION"
    URL_VALIDATION = "URL_VALIDATION"
    MTI_VALIDATION = "MTI_VALIDATION"
    LUHN_VALIDATION = "LUHN_VALIDATION"
    FIELDS_VALIDATION = "FIELDS_VALIDATION"
    FIELD_NUMBER_VALIDATION = "FIELD_NUMBER_VALIDATION"
    FIELD_PATH_VALIDATION = "FIELD_PATH_VALIDATION"
    FIELD_DATA_VALIDATION = "FIELD_DATA_VALIDATION"
    COUNTRY_VALIDATION = "COUNTRY_VALIDATION"
    CURRENCY_VALIDATION = "CURRENCY_VALIDATION"


class ValidationResult(BaseModel):
    errors: dict[ValidationTypes, set[str]] = dict.fromkeys([validation for validation in ValidationTypes])

    critical_validation_types: list[ValidationTypes] = [
        ValidationTypes.FIELD_DATA_PRE_VALIDATION,
        ValidationTypes.FIELD_DATA_MAIN_VALIDATION,
        ValidationTypes.MTI_VALIDATION,
    ]
