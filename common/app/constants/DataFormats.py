from dataclasses import dataclass


@dataclass
class DataFormats:
    INI: str = "INI"
    JSON: str = "JSON"
    DUMP: str = "DUMP"
    SPEC: str = "SPEC"
    TXT: str = "TXT"
    OTHER: str = "OTHER"
    SV_TERMINAL: str = "TERMINAL"

    @staticmethod
    def get_print_data_formats():
        return (
            DataFormats.JSON,
            DataFormats.INI,
            DataFormats.DUMP,
            DataFormats.SPEC,
            DataFormats.SV_TERMINAL
        )

    @staticmethod
    def get_input_file_formats():
        return (
            DataFormats.JSON,
            DataFormats.INI,
            DataFormats.TXT
        )

    @staticmethod
    def get_output_file_formats():
        return (
            DataFormats.JSON,
            DataFormats.INI,
            DataFormats.DUMP
        )
