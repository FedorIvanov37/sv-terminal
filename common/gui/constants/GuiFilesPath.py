from pydantic import DirectoryPath, FilePath
from common.lib.constants import TermFilesPath


STYLE_DIR: DirectoryPath = f"{TermFilesPath.DATA_DIR}/style"

MAIN_LOGO: FilePath = f"{STYLE_DIR}/logo_triangle.png"
MUSIC_ON: FilePath = f"{STYLE_DIR}/music_on.png"
MUSIC_OFF: FilePath = f"{STYLE_DIR}/music_off.png"
VVVVVV: FilePath = f"{STYLE_DIR}/VVVVVV.mp3"
GIF_ABOUT: FilePath = f"{STYLE_DIR}/rocks.gif"

GREEN_CIRCLE: FilePath = f"{STYLE_DIR}/green_circle.ico"
GREY_CIRCLE: FilePath = f"{STYLE_DIR}/grey_circle.ico"
RED_CIRCLE: FilePath = f"{STYLE_DIR}/red_circle.ico"
YELLOW_CIRCLE: FilePath = f"{STYLE_DIR}/yellow_circle.ico"
