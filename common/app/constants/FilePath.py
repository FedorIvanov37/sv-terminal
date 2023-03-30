from dataclasses import dataclass
from pydantic import FilePath, DirectoryPath


@dataclass(frozen=True)
class FilePath(object):
    CONFIG: FilePath = "common/settings/config.json"
    ECHO_TEST: FilePath = "common/settings/echo-test.json"
    DEFAULT_FILE: FilePath = "common/settings/default.json"
    SPECIFICATION: FilePath = "common/settings/specification.json"
    LOG_FILE_NAME: FilePath = "common/log/sv_terminal.log"
    MAIN_LOGO: FilePath = "common/app/style/logo_triangle.png"
    SPEC_BACKUP_DIR: DirectoryPath = "common/backup"
