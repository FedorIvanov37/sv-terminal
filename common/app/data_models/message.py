from uuid import uuid1 as uuid
from pydantic import BaseModel, Field, UUID1, validator
from common.app.core.tools.validator import Validator


TypeFields = dict[str, str | dict]


class MessageConfig(BaseModel):
    generate_fields: list[str] = list()
    max_amount: str = "100"

    @validator("max_amount")
    def amount_should_be_digit(cls, max_amount: str):
        max_amount = str(max_amount)

        if not max_amount.isdigit():
            raise ValueError("Max transaction amount should be digits only")

        return max_amount


class TransactionModel(BaseModel):
    id: str = str()
    original_id: str = str()
    external_id: UUID1 = Field(default_factory=lambda: str(uuid()))
    utrnno: str = str()
    message_type: str
    fields: TypeFields

    @validator("fields")
    def respect_specification(cls, fields: TypeFields):
        message_validator = Validator()
        return message_validator.validate_fields(fields)


class Message(BaseModel):
    config: MessageConfig = MessageConfig()
    transaction: TransactionModel


class TransMod(BaseModel):
    trans_id: str = ""
    match_id: str = ""
    generate_fields: list[str] = []
    max_amount: str = "100"
    message_type: str = ""
    utrnno: str = ""
    data_fields: dict[str, str | dict]