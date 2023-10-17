class DataFormats(object):
    INI: str = "INI"
    JSON: str = "JSON"
    DUMP: str = "DUMP"
    SPEC: str = "SPEC"
    TXT: str = "TXT"
    OTHER: str = "OTHER"
    TERM: str = "SIGNAL"

    @staticmethod
    def get_print_data_formats():
        return (
            DataFormats.JSON,
            DataFormats.INI,
            DataFormats.DUMP,
            DataFormats.SPEC,
            DataFormats.TERM
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
