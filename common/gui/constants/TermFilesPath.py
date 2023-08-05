from dataclasses import dataclass
from pydantic import DirectoryPath, FilePath


@dataclass(frozen=True)
class TermFilesPath(object):
    DATA_DIR: DirectoryPath = "common"
    STYLE_DIR: DirectoryPath = "common/style"
    SPEC_BACKUP_DIR: DirectoryPath = f"{DATA_DIR}/spec_backup"

    CONFIG: FilePath = f"{DATA_DIR}/settings/config.json"
    ECHO_TEST: FilePath = f"{DATA_DIR}/settings/echo-test.json"
    KEEP_ALIVE: FilePath = f"{DATA_DIR}/settings/keep-alive.json"
    DEFAULT_FILE: FilePath = f"{DATA_DIR}/settings/default.json"
    SPECIFICATION: FilePath = f"{DATA_DIR}/settings/specification.json"
    LOG_FILE_NAME: FilePath = f"{DATA_DIR}/log/sv_terminal.log"

    MAIN_LOGO: FilePath = f"{STYLE_DIR}/logo_triangle.png"
    MUSIC_ON: FilePath = f"{STYLE_DIR}/music_on.png"
    MUSIC_OFF: FilePath = f"{STYLE_DIR}/music_off.png"
    VVVVVV: FilePath = f"{STYLE_DIR}/VVVVVV.mp3"
    GIF_ABOUT: FilePath = f"{STYLE_DIR}/rocks.gif"

    GREEN_CIRCLE: FilePath = f"{STYLE_DIR}/green_circle.ico"
    GREY_CIRCLE: FilePath = f"{STYLE_DIR}/grey_circle.ico"
