from dataclasses import dataclass
from pydantic import DirectoryPath, FilePath


@dataclass(frozen=True)
class TermFilesPath(object):
    DATA_DIR: DirectoryPath = "common/data"
    LOG_DIR: DirectoryPath = "common/log"
    SPEC_BACKUP_DIR: DirectoryPath = f"{DATA_DIR}/spec_backup"
    #
    CONFIG: FilePath = f"{DATA_DIR}/settings/config.json"
    ECHO_TEST: FilePath = f"{DATA_DIR}/settings/echo-test.json"
    KEEP_ALIVE: FilePath = f"{DATA_DIR}/settings/keep-alive.json"
    DEFAULT_FILE: FilePath = f"{DATA_DIR}/settings/default.json"
    SPECIFICATION: FilePath = f"{DATA_DIR}/settings/specification.json"
    LOG_FILE_NAME: FilePath = f"{LOG_DIR}/signal.log"
