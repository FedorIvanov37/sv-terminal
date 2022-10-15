from dataclasses import dataclass


@dataclass
class FilePath:
    CONFIG: str = r"common\settings\config.json"
    ECHO_TEST: str = r"common\settings\echo-test.json"
    DEFAULT_FILE: str = r"common\settings\default.json"
    SPECIFICATION: str = r"C:\fedor\sv_terminal\v0.15\common\settings\specification.json"
    MAIN_LOGO: str = r"common\app\style\logo_triangle.png"
    RUN_SCRIPT = "sv_terminal.pyw"
    SPEC_BACKUP_DIR = r"common\backup"
    LOG_FILE_NAME: str = r"common\log\sv_terminal.log"
    VVVVVV: str = r"C:\fedor\sv_terminal\v0.13\common\style\VVVVVV.mp3"
