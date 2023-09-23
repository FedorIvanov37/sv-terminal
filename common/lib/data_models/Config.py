from pydantic import BaseModel, validator


class Host(BaseModel):
    host: str = str()
    port: int = int()
    keep_alive_mode: bool = False
    keep_alive_interval: int = 300
    header_length: int = 0
    header_length_exists: bool = True


class Terminal(BaseModel):
    process_default_dump: bool = True
    connect_on_startup: bool = True


class Debug(BaseModel):
    level: str = "INFO"
    clear_log: bool = True
    parse_subfields: bool = False


class Fields(BaseModel):
    max_amount: int
    max_amount_limited: bool
    build_fld_90: bool = True
    send_internal_id: bool = True
    validation: bool = True
    json_mode: bool = True
    hide_secrets: bool = True

    @validator("max_amount", pre=True)
    def amount_should_be_digit(cls, max_amount: str):
        if not str(max_amount).isdigit():
            raise ValueError("Max transaction amount should be digits only")

        return int(max_amount)


class Config(BaseModel):
    host: Host
    terminal: Terminal
    debug: Debug
    fields: Fields | None = None
