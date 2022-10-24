from dataclasses import dataclass


@dataclass(frozen=True)
class FilePath(object):
    CONFIG = "common/settings/config.json"
    ECHO_TEST = "common/settings/echo-test.json"
    DEFAULT_FILE = "common/settings/default.json"
    SPECIFICATION = "common/settings/specification.json"
    LOG_FILE_NAME = "common/log/sv_terminal.log"
    MAIN_LOGO = "common/app/style/logo_triangle.png"
