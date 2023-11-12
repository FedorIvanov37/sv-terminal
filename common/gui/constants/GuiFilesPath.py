from typing import Final
from pydantic import DirectoryPath, FilePath
from common.lib.constants import TermFilesPath


STYLE_DIR: Final[DirectoryPath] = f"{TermFilesPath.DATA_DIR}/style"

MAIN_LOGO: Final[FilePath] = f"{STYLE_DIR}/logo_triangle.png"
MUSIC_ON: Final[FilePath] = f"{STYLE_DIR}/music_on.png"
MUSIC_OFF: Final[FilePath] = f"{STYLE_DIR}/music_off.png"
VVVVVV: Final[FilePath] = f"{STYLE_DIR}/VVVVVV.mp3"
GIF_ABOUT: Final[FilePath] = f"{STYLE_DIR}/rocks.gif"

GREEN_CIRCLE: Final[FilePath] = f"{STYLE_DIR}/green_circle.ico"
GREY_CIRCLE: Final[FilePath] = f"{STYLE_DIR}/grey_circle.ico"
RED_CIRCLE: Final[FilePath] = f"{STYLE_DIR}/red_circle.ico"
YELLOW_CIRCLE: Final[FilePath] = f"{STYLE_DIR}/yellow_circle.ico"
