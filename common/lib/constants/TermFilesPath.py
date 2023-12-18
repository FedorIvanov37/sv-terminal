from typing import Final
from pydantic import DirectoryPath, FilePath


DATA_DIR: Final[DirectoryPath] = "common/data"
LOG_DIR: Final[DirectoryPath] = "common/log"

SPEC_BACKUP_DIR: Final[DirectoryPath] = f"{DATA_DIR}/spec_backup"
DEFAULT_MSG_DIR: Final[DirectoryPath] = f"{DATA_DIR}/default"
LICENSE_DIR: Final[DirectoryPath] = f"{DATA_DIR}/license"
CONFIG_DIR: Final[DirectoryPath] = f"{DATA_DIR}/settings"
DICTIONARY_DIR: Final[DirectoryPath] = f"{DATA_DIR}/dictionary"

CONFIG: Final[FilePath] = f"{CONFIG_DIR}/config.json"
DEFAULT_CONFIG: Final[FilePath] = f"{CONFIG_DIR}/default_config.json"
SPECIFICATION: Final[FilePath] = f"{CONFIG_DIR}/specification.json"
ECHO_TEST: Final[FilePath] = f"{DEFAULT_MSG_DIR}/echo-test.json"
KEEP_ALIVE: Final[FilePath] = f"{DEFAULT_MSG_DIR}/keep-alive.json"
DEFAULT_FILE: Final[FilePath] = f"{DEFAULT_MSG_DIR}/default_message.json"
LICENSE_INFO: Final[FilePath] = f"{LICENSE_DIR}/license_info.json"
LOG_FILE_NAME: Final[FilePath] = f"{LOG_DIR}/signal.log"

CURRENCY_DICT: Final[FilePath] = f"{DICTIONARY_DIR}/currencies.json"
COUNTRY_DICT: Final[FilePath] = f"{DICTIONARY_DIR}/countries.json"
MCC_DICT: Final[FilePath] = f"{DICTIONARY_DIR}/merch_categories.json"
