INI: str = "INI"
JSON: str = "JSON"
DUMP: str = "DUMP"
SPEC: str = "SPEC"
TXT: str = "TXT"
OTHER: str = "OTHER"
TERM: str = "SIGNAL"


def get_print_data_formats():
    return JSON, INI, DUMP, SPEC, TERM


def get_input_file_formats():
    return JSON, INI, TXT


def get_output_file_formats():
    return JSON, INI, DUMP
