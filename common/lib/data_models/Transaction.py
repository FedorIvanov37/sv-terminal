from pydantic import BaseModel


TypeFields = dict[str, str | dict]


class Transaction(BaseModel):
    trans_id: str = ""
    match_id: str = str()
    utrnno: str = str()
    message_type: str = str()
    matched: bool | None = None
    success: bool | None = None
    max_amount: str = "100"
    resp_time_seconds: float | None = None
    generate_fields: list[str] = []
    data_fields: dict = {}
    is_request: bool | None = None
    is_reversal: bool | None = None
    is_keep_alive: bool = False
