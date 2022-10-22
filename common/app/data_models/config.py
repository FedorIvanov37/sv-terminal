from pydantic import BaseModel


class SmartVista(BaseModel):
    host: str = str()
    port: str = str()
    api_port: str = str()


class Terminal(BaseModel):
    process_default_dump: bool = True
    connect_on_startup: bool = True
    run_api: bool = False


class Debug(BaseModel):
    level: str = "INFO"
    clear_log: bool = True
    parse_subfields: bool = False


class Fields(BaseModel):
    max_amount: int = 1000
    build_fld_90: bool = False
    send_internal_id: bool = False
    validation: bool = False


class Config(BaseModel):
    smartvista: SmartVista = SmartVista()
    terminal: Terminal = Terminal()
    debug: Debug = Debug()
    fields: Fields | None = None
