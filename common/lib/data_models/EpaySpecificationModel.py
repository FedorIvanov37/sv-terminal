from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import ForwardRef
from enum import Enum


FieldSet = dict[str, ForwardRef("IsoField")]
RawFieldSet = dict[str, str | dict]
MtiValue = Field(default="", max_length=4, pattern=r"^\d{4}|$")
literal_list = list[str]


class FieldTypes(str, Enum):
    COUNTRY_CODE = "COUNTRY CODE"
    CURRENCY_CODE = "CURRENCY CODE"
    MERCHANT_CATEGORY_CODE = "MERCHANT CATEGORY CODE"
    DATE = "DATE"


class Justification(str, Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class ValidationTypes(str, Enum):
    MUST_NOT_CONTAIN = "must_not_contain"
    POSSIBLE_VALUES = "possible_values"
    MUST_START_WITH = "must_start_with"
    MUST_END_WITH = "must_end_with"
    MUST_CONTAIN = "must_contain"
    VALID_VALUES = "valid_values"
    INVALID_VALUES = "invalid_values"
    MUST_CONTAIN_ONLY = "must_contain_only"
    MUST_NOT_END_WITH = "must_not_end_with"
    MUST_NOT_START_WITH = "must_not_start_with"
    MUST_NOT_CONTAIN_ONLY = "must_not_contain_only"


class Mti(BaseModel):
    request: str = MtiValue
    response: str = MtiValue
    description: str = str()
    is_reversible: bool = False
    reversal_mti: str = MtiValue


class Validators(BaseModel):
    field_type: FieldTypes | None = None
    date_format: str | None = None
    must_not_contain: literal_list = list()
    possible_values: literal_list = list()
    must_start_with: literal_list = list()
    must_end_with: literal_list = list()
    must_contain: literal_list = list()
    valid_values: literal_list = list()
    invalid_values: literal_list = list()
    must_contain_only: literal_list = list()
    must_not_end_with: literal_list = list()
    must_not_start_with: literal_list = list()
    must_not_contain_only: literal_list = list()
    justification: Justification | None = None
    justification_element: str | None = None
    justification_length: int = 0
    min_value: int = 0
    max_value: int = 0

class IsoField(BaseModel):
    model_config: ConfigDict = ConfigDict(validate_assignment=True)

    validators: Validators | None = Validators()
    field_number: str = ""
    field_path: list = []
    min_length: int
    max_length: int
    var_length: int
    tag_length: int
    generate: bool
    reversal: bool
    matching: bool
    alpha: bool
    numeric: bool
    special: bool
    reserved_for_future: bool
    description: str = str()
    is_secret: bool = False
    fields: FieldSet | None = None

    @field_validator("is_secret", mode="before")
    @classmethod
    def substitute_none_by_bool(cls, val):
        if val is None:
            return False

        return val

    @field_validator("validators", mode="before")
    @classmethod
    def substitute_none_validator(cls, val):
        if val is None:
            return Validators()

        return val


class EpaySpecModel(BaseModel):
    name: str | None = "ISO-8583 E-pay Specification"
    mti: list[Mti] = []
    fields: FieldSet = {}
