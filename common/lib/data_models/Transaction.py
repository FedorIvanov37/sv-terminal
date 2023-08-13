from pydantic import BaseModel
from common.lib.core.EpaySpecification import EpaySpecification
# from common.lib.data_models.Enums import message_type_indicator, generated_field


spec: EpaySpecification = EpaySpecification()
TypeFields = dict[str, str | dict]


class Transaction(BaseModel):
    class Config:
        use_enum_values = True

    trans_id: str = ""
    match_id: str = str()
    utrnno: str = str()
    message_type: str = ""  # message_type_indicator
    matched: bool | None = None
    success: bool | None = None
    max_amount: int = "100"
    resp_time_seconds: float | None = None
    generate_fields: list[str] = [] # list[generated_field] = []
    data_fields: dict
    is_request: bool | None = None
    is_reversal: bool | None = None
    is_keep_alive: bool = False


class OldTransaction(BaseModel):
    id: str = ""
    original_id: str = ""
    message_type: str = ""
    fields: TypeFields


class OldTransactionConfig(BaseModel):
    generate_fields: list[str] = []
    max_amount: str


class OldTransactionModel(BaseModel):
    config: OldTransactionConfig
    transaction: OldTransaction
