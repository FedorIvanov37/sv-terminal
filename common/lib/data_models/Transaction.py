from datetime import datetime
from pydantic import BaseModel, Field, validator
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.toolkit.generate_trans_id import generate_trans_id
from common.lib.constants.MessageLength import MessageLength
from common.lib.data_models.Enums import generated_field


spec: EpaySpecification = EpaySpecification()
TypeFields = dict[str, str | dict]


class Transaction(BaseModel):
    class Config:
        use_enum_values = True
        validate_assignment = True

    trans_id: str = Field(default_factory=generate_trans_id)
    message_type: str
    data_fields: TypeFields
    max_amount: int = 100
    generate_fields: list[generated_field] = []

    match_id: str = str()
    utrnno: str = str()
    matched: bool | None = None
    success: bool | None = None
    resp_time_seconds: float | None = None
    sending_time: datetime | None = None
    is_request: bool | None = None
    is_reversal: bool | None = None
    is_keep_alive: bool = False

    @validator("max_amount", pre=True)
    def check_amount(cls, val):
        error_message = f"Wrong max_amount {val}. Amount must be digit in range from 0 to 999 999 999"

        if not str(val).isdigit():
            raise TypeError(error_message)

        if int(val) not in range(0, 1000000000):
            raise ValueError(error_message)

        return val

    @validator("generate_fields", pre=True)
    def field_to_str(cls, val):
        return [str(field) for field in val]

    @validator("trans_id")
    def generate_transaction_id(cls, val):
        if not val:
            return generate_trans_id()

        return val

    @validator("message_type")
    def valid_mti(cls, val: str):
        if len(str(val)) != MessageLength.message_type_length:
            raise ValueError(f"Incorrect MTI length. Expected {MessageLength.message_type_length}, got {len(str(val))}")

        if not val.isdigit():
            raise TypeError(f"Wrong MTI value {val}. MTI must contain digits only")

        if val not in spec.get_mti_codes():
            raise ValueError(f"No specification for MTI {val}. Correct MTI or set it in Specification Window")

        return val

    @validator("data_fields")
    def top_level_fields_in_range(cls, val: TypeFields):
        for field in val.keys():
            if not field.isdigit():
                raise TypeError(f"Incorrect field number {field}. Field numbers must contain digits only")

            if int(field) not in range(1, MessageLength.second_bitmap_capacity + 1):
                raise ValueError(f"Wrong field number {field}. " 
                                 f"Top level fields must be in range 1 - {MessageLength.second_bitmap_capacity}")
        return val


class OldTransaction(BaseModel):
    id: str = Field(default_factory=generate_trans_id)
    original_id: str = ""
    message_type: str = ""
    fields: TypeFields


class OldTransactionConfig(BaseModel):
    class Config:
        use_enum_values = True

    generate_fields: list[generated_field] = []
    max_amount: int | None = None

    @validator("generate_fields", pre=True)
    def field_to_str(cls, val):
        return [str(field) for field in val]


class OldTransactionModel(BaseModel):
    config: OldTransactionConfig
    transaction: OldTransaction
