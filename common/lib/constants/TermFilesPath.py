from typing import Final
from pydantic import DirectoryPath, FilePath


DATA_DIR: Final[DirectoryPath] = "common/data"
LOG_DIR: Final[DirectoryPath] = "common/log"
SPEC_BACKUP_DIR: Final[DirectoryPath] = f"{DATA_DIR}/spec_backup"

CONFIG: Final[FilePath] = f"{DATA_DIR}/settings/config.json"
DEFAULT_CONFIG: Final[FilePath] = f"{DATA_DIR}/settings/default_config.json"
ECHO_TEST: Final[FilePath] = f"{DATA_DIR}/settings/echo-test.json"
KEEP_ALIVE: Final[FilePath] = f"{DATA_DIR}/settings/keep-alive.json"
DEFAULT_FILE: Final[FilePath] = f"{DATA_DIR}/settings/default_message.json"
SPECIFICATION: Final[FilePath] = f"{DATA_DIR}/settings/specification.json"
LICENSE_INFO: Final[FilePath] = f"{DATA_DIR}/settings/license_info.json"
LOG_FILE_NAME: Final[FilePath] = f"{LOG_DIR}/signal.log"
