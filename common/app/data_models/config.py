from pydantic import BaseModel
from typing import Optional


class SmartVista(BaseModel):
    host: str = str()
    port: str = str()
    api_port: str = str()
    # use_proxy: bool = False


class Terminal(BaseModel):
    process_default_dump: bool = True
    connect_on_startup: bool = True
    run_api: bool = False


class Debug(BaseModel):
    level: str
    clear_log: bool = True
    parse_subfields: bool = False


class Fields(BaseModel):
    max_amount: int = 1000
    build_fld_90: bool = False
    send_internal_id: bool = False


class Config(BaseModel):
    smartvista: SmartVista
    terminal: Terminal
    debug: Debug
    fields: Optional[Fields] = None
