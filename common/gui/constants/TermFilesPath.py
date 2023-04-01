from dataclasses import dataclass
from pydantic import DirectoryPath, FilePath


@dataclass(frozen=True)
class TermFilesPath(object):
    DATA_DIR: DirectoryPath = "common/data"
    STYLE_DIR: DirectoryPath = "common/gui/style"
    SPEC_BACKUP_DIR: DirectoryPath = f"{DATA_DIR}/spec_backup"

    CONFIG: FilePath = f"{DATA_DIR}/settings/config.json"
    ECHO_TEST: FilePath = f"{DATA_DIR}/settings/echo-test.json"
    DEFAULT_FILE: FilePath = f"{DATA_DIR}/settings/default.json"
    SPECIFICATION: FilePath = f"{DATA_DIR}/settings/specification.json"
    LOG_FILE_NAME: FilePath = f"{DATA_DIR}/log/sv_terminal.log"

    MAIN_LOGO: FilePath = f"{STYLE_DIR}/logo_triangle.png"
    MUSIC_ON: FilePath = f"{STYLE_DIR}/music_on.png"
    MUSIC_OFF: FilePath = f"{STYLE_DIR}/music_off.png"
    VVVVVV: FilePath = f"{STYLE_DIR}/VVVVVV.mp3"
    GIF_ABOUT: FilePath = f"{STYLE_DIR}/rocks.gif"
