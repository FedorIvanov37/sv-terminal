from enum import StrEnum


class TermDirs(StrEnum):
    DATA_DIR = "signal/data"
    LOG_DIR = "signal/log"
    SPEC_BACKUP_DIR = f"{DATA_DIR}/spec_backup"
    DEFAULT_MSG_DIR = f"{DATA_DIR}/default"
    LICENSE_DIR = f"{DATA_DIR}/license"
    CONFIG_DIR = f"{DATA_DIR}/settings"
    DICTIONARY_DIR = f"{DATA_DIR}/dictionary"


class TermFiles(StrEnum):
    CONFIG = "config.json"
    DEFAULT_CONFIG = "default_config.json"
    SPECIFICATION = "specification.json"
    ECHO_TEST = "echo-test.json"
    KEEP_ALIVE = "keep-alive.json"
    DEFAULT_FILE = "default_message.json"
    LICENSE_INFO = "license_info.json"
    LOG_FILE_NAME = "signal.log"
    CURRENCY_DICT = "currencies.json"
    COUNTRY_DICT = "countries.json"
    MCC_DICT = "merch_categories.json"


class TermFilesPath(StrEnum):
    CONFIG = f"{TermDirs.CONFIG_DIR}/{TermFiles.CONFIG}"
    DEFAULT_CONFIG = f"{TermDirs.CONFIG_DIR}/{TermFiles.DEFAULT_CONFIG}"
    SPECIFICATION = f"{TermDirs.CONFIG_DIR}/{TermFiles.SPECIFICATION}"
    ECHO_TEST = f"{TermDirs.DEFAULT_MSG_DIR}/{TermFiles.ECHO_TEST}"
    KEEP_ALIVE = f"{TermDirs.DEFAULT_MSG_DIR}/{TermFiles.KEEP_ALIVE}"
    DEFAULT_FILE = f"{TermDirs.DEFAULT_MSG_DIR}/{TermFiles.DEFAULT_FILE}"
    LICENSE_INFO = f"{TermDirs.LICENSE_DIR}/{TermFiles.LICENSE_INFO}"
    LOG_FILE_NAME = f"{TermDirs.LOG_DIR}/{TermFiles.LOG_FILE_NAME}"
    CURRENCY_DICT = f"{TermDirs.DICTIONARY_DIR}/{TermFiles.COUNTRY_DICT}"
    COUNTRY_DICT = f"{TermDirs.DICTIONARY_DIR}/{TermFiles.COUNTRY_DICT}"
    MCC_DICT = f"{TermDirs.DICTIONARY_DIR}/{TermFiles.MCC_DICT}"
