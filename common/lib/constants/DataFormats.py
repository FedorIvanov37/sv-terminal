from typing import Final


INI: Final[str] = "INI"
JSON: Final[str] = "JSON"
DUMP: Final[str] = "DUMP"
SPEC: Final[str] = "SPEC"
TXT: Final[str] = "TXT"
OTHER: Final[str] = "OTHER"
TERM: Final[str] = "SIGNAL"


def get_print_data_formats():
    return JSON, INI, DUMP, SPEC, TERM


def get_input_file_formats():
    return JSON, INI, TXT


def get_output_file_formats():
    return JSON, INI, DUMP
