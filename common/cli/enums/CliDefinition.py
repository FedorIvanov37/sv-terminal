from enum import StrEnum


class CliDefinition(StrEnum):
    CONSOLE_MODE = "-c"
    CONSOLE_MODE_LONG = "--console"
    HELP = "-h"
    HELP_LONG = "--help"
