from pydantic import BaseModel, Field


FieldSet = dict[str, "IsoField"]
RawFieldSet = dict[str, str | dict]
MtiValue = Field(default="", max_length=4, regex=r"^\d{4}|$")


class Mti(BaseModel):
    request: str = MtiValue
    response: str = MtiValue
    description: str = str()
    is_reversible: bool = False
    reversal_mti: str = MtiValue


class IsoField(BaseModel):
    min_length: int = int()
    max_length: int = int()
    var_length: int = int()
    tag_length: int = int()
    generate: bool = False
    reversal: bool = False
    matching: bool = False
    alpha: bool = False
    numeric: bool = False
    special: bool = False
    bytes: bool = False
    reserved_for_future: bool = False
    description: str = str()
    is_secret: bool = False
    fields: FieldSet | None


class EpaySpecModel(BaseModel):
    name: str | None = "ISO-8583 E-pay Specification"
    mti: list[Mti] = Field(min_items=1, alias="mti")
    fields: FieldSet = {}
