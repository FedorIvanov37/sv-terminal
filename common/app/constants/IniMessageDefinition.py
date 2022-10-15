from dataclasses import dataclass


@dataclass
class IniMessageDefinition:
    MTI = "MTI"
    MESSAGE = "MESSAGE"
    CONFIG = "CONFIG"
    GENERATE_FIELDS = "GENERATE_FIELDS"
    MAX_AMOUNT = "MAX_AMOUNT"
