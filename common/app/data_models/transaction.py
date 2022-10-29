from pydantic import BaseModel, Field
from common.app.core.tools.trans_id import trans_id

TypeFields = dict[str, str | dict]


class Transaction(BaseModel):
    message_type: str = ""
    trans_id: str = Field(default_factory=trans_id)
    match_id: str = ""
    generate_fields: list[str] = []
    data_fields: TypeFields = {}
    max_amount: str = "100"
    matched: bool = False
    utrnno: str = str()
