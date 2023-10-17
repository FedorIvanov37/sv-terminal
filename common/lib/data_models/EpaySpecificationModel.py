from pydantic import BaseModel, Field, field_validator


FieldSet = dict[str, "IsoField"]
RawFieldSet = dict[str, str | dict]
MtiValue = Field(default="", max_length=4, pattern=r"^\d{4}|$")


class Mti(BaseModel):
    request: str = MtiValue
    response: str = MtiValue
    description: str = str()
    is_reversible: bool = False
    reversal_mti: str = MtiValue


class IsoField(BaseModel):
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

    @field_validator("is_secret", mode='before')
    def substitute_none(cls, val):
        if val is None:
            return False

        return val


class EpaySpecModel(BaseModel):
    name: str | None = "ISO-8583 E-pay Specification"
    mti: list[Mti] = Field(min_items=1, alias="mti")
    fields: FieldSet = {}
