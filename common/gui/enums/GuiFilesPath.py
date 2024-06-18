from enum import StrEnum
from common.lib.enums.TermFilesPath import TermDirs


class GuiDirs(StrEnum):
    STYLE_DIR = f"{TermDirs.DATA_DIR}/style"


class GuiFiles(StrEnum):
    MAIN_LOGO = "triforce_unsigned.png"
    SIGNED_LOGO = "triforce_signed.png"
    MUSIC_ON = "music_on.png"
    MUSIC_OFF = "music_off.png"
    VVVVVV = "VVVVVV.mp3"
    GREEN_CIRCLE = "green_circle.ico"
    GREY_CIRCLE = "grey_circle.ico"
    RED_CIRCLE = "red_circle.ico"
    YELLOW_CIRCLE = "yellow_circle.ico"
    NEW_TAB = "new_tab.ico"


class GuiFilesPath(StrEnum):
    M_LOGO = f"{GuiDirs.STYLE_DIR.name}:{GuiFiles.MAIN_LOGO}"
    G_CIRCLE = ":".join([GuiDirs.STYLE_DIR.name, GuiFiles.GREEN_CIRCLE])
    MAIN_LOGO = f"{GuiDirs.STYLE_DIR}/{GuiFiles.MAIN_LOGO}"
    SIGNED_LOGO = f"{GuiDirs.STYLE_DIR}/{GuiFiles.SIGNED_LOGO}"
    MUSIC_ON = f"{GuiDirs.STYLE_DIR}/{GuiFiles.MUSIC_ON}"
    MUSIC_OFF = f"{GuiDirs.STYLE_DIR}/{GuiFiles.MUSIC_OFF}"
    VVVVVV = f"{GuiDirs.STYLE_DIR}/{GuiFiles.VVVVVV}"
    GREEN_CIRCLE = f"{GuiDirs.STYLE_DIR}/{GuiFiles.GREEN_CIRCLE}"
    GREY_CIRCLE = f"{GuiDirs.STYLE_DIR}/{GuiFiles.GREY_CIRCLE}"
    RED_CIRCLE = f"{GuiDirs.STYLE_DIR}/{GuiFiles.RED_CIRCLE}"
    YELLOW_CIRCLE = f"{GuiDirs.STYLE_DIR}/{GuiFiles.YELLOW_CIRCLE}"
    NEW_TAB = f"{GuiDirs.STYLE_DIR}/{GuiFiles.NEW_TAB}"
