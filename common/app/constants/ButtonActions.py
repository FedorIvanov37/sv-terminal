from dataclasses import dataclass


@dataclass
class ButtonAction:
    LAST = "Last"
    OTHER = "Other"

    @staticmethod
    def get_reversal_actions():
        return ButtonAction.LAST, ButtonAction.OTHER
