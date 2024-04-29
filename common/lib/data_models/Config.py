from pydantic import BaseModel, field_validator
from common.lib.enums.Validation import ValidationMode


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
    load_remote_spec: bool = False
    show_license_dialog: bool = True


class Debug(BaseModel):
    level: str = "INFO"
    clear_log: bool = True
    parse_subfields: bool = False
    backup_storage_depth: int = 30


class Validation(BaseModel):
    validation_enabled: bool = True
    validate_window: bool = True
    validate_incoming: bool = False
    validate_outgoing: bool = True
    validation_mode: ValidationMode = ValidationMode.ERROR


class Fields(BaseModel):
    max_amount: int
    max_amount_limited: bool
    build_fld_90: bool = True
    send_internal_id: bool = True
    json_mode: bool = True
    hide_secrets: bool = True

    @field_validator("max_amount", mode='before')
    @classmethod
    def amount_should_be_digit(cls, max_amount: str):
        if not str(max_amount).isdigit():
            raise ValueError("Max transaction amount should be digits only")

        return int(max_amount)


class Specification(BaseModel):
    rewrite_local_spec: bool = False
    remote_spec_url: str = str()
    backup_storage_depth: int = 100
    backup_storage: bool = True
    manual_input_mode: bool = False


class Config(BaseModel):
    host: Host
    terminal: Terminal
    debug: Debug
    validation: Validation = None
    fields: Fields | None = None
    specification: Specification = Specification()
