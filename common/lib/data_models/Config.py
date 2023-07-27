from pydantic import BaseModel, validator


class SmartVista(BaseModel):
    host: str = str()
    port: str = str()


class Terminal(BaseModel):
    process_default_dump: bool = True
    connect_on_startup: bool = True


class Debug(BaseModel):
    level: str = "INFO"
    clear_log: bool = True
    parse_subfields: bool = False


class Fields(BaseModel):
    max_amount: str = "1000"
    build_fld_90: bool = False
    send_internal_id: bool = False
    validation: bool = False
    flat_mode: bool = False

    @validator("max_amount")
    def amount_should_be_digit(cls, max_amount: str):
        max_amount = str(max_amount)

        if not max_amount.isdigit():
            raise ValueError("Max transaction amount should be digits only")

        return max_amount


class Config(BaseModel):
    smartvista: SmartVista = SmartVista()
    terminal: Terminal = Terminal()
    debug: Debug = Debug()
    fields: Fields | None = None
