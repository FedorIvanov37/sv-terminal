from dataclasses import dataclass


@dataclass
class DumpDefinition:
    LINE_LENGTH = 32
    HEX_LINE_LENGTH = 51
    ASCII_LINE_LENGTH = 16
    BYTE_LENGTH = 2
    SEPARATOR = "."
    ASCII_BITMAP = "........"
