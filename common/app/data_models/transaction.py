from pydantic import BaseModel


TypeFields = dict[str, str | dict]


class Transaction(BaseModel):
    trans_id: str = str()
    match_id: str = str()
    utrnno: str = str()
    matched: bool = False
    generate_fields: list[str] = []
    max_amount: str = "100"
    message_type: str = ""
    data_fields: TypeFields = {}
