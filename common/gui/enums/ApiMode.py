from enum import StrEnum


class ApiModes(StrEnum):
    START = "START"
    STOP = "STOP"
    NOT_RUN = "NOT_RUN"


class ApiModeNames(StrEnum):
    START = "API mode started"
    STOP = "API mode stop"
    NOT_RUN = "API mode not started"
