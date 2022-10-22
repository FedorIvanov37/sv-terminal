from pydantic import BaseModel, Field, UUID1, validator
from uuid import uuid1 as uuid
from common.app.core.tools.validator import Validator


TypeFields = dict[str, str | dict]
TerminalValidator = Validator()


class MessageConfig(BaseModel):
    generate_fields: list[str] = list()
    max_amount: int = 100


class TransactionModel(BaseModel):
    id: str = str()
    original_id: str = str()
    external_id: UUID1 = Field(default_factory=lambda: str(uuid()))
    utrnno: str = str()
    message_type: str
    fields: TypeFields

    @validator("fields")
    def respect_specification(cls, fields: TypeFields):
        return TerminalValidator.validate_fields(fields)


class Message(BaseModel):
    config: MessageConfig = MessageConfig()
    transaction: TransactionModel
