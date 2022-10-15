from pydantic import BaseModel, Field, UUID1
from uuid import uuid1 as uuid


TypeFields = dict[str, str | dict]


class MessageConfig(BaseModel):
    generate_fields: list[str] = list()
    max_amount: int = 100


class TransactionModel(BaseModel):
    id: str = str()
    original_id: str = str()
    external_id: UUID1 = Field(default_factory=lambda: str(uuid()))
    utrnno: str = str()
    message_type_indicator: str
    fields: TypeFields


class Message(BaseModel):
    config: MessageConfig = MessageConfig()
    transaction: TransactionModel
