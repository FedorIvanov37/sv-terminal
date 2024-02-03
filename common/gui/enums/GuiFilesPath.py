from enum import StrEnum
from common.lib.enums.TermFilesPath import TermDirs


class GuiFilesPath(StrEnum):
    STYLE_DIR = f"{TermDirs.DATA_DIR}/style"
    MAIN_LOGO = f"{STYLE_DIR}/logo_triangle.png"
    MUSIC_ON = f"{STYLE_DIR}/music_on.png"
    MUSIC_OFF = f"{STYLE_DIR}/music_off.png"
    VVVVVV = f"{STYLE_DIR}/VVVVVV.mp3"
    GIF_ABOUT = f"{STYLE_DIR}/rocks.gif"
    GREEN_CIRCLE = f"{STYLE_DIR}/green_circle.ico"
    GREY_CIRCLE = f"{STYLE_DIR}/grey_circle.ico"
    RED_CIRCLE = f"{STYLE_DIR}/red_circle.ico"
    YELLOW_CIRCLE = f"{STYLE_DIR}/yellow_circle.ico"
