from pydantic import BaseModel, DirectoryPath, IPvAnyAddress
from common.lib.constants.LogDefinition import DebugLevels


class CliConfig(BaseModel):
    console_mode: bool = False
    file: str | None = None
    dir: DirectoryPath | None = None
    address: IPvAnyAddress
    port: int
    repeat: bool = False
    log_level: str = DebugLevels.INFO
    interval: int = 1
    parallel: bool = False
    timeout: int = 60
    echo_test: bool = False
    about: bool = False
    default: bool = False
    version: bool = False
    config: bool = False
