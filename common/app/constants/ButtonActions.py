from dataclasses import dataclass


@dataclass
class ButtonAction(object):
    LAST = "Last"
    OTHER = "Other"

    @staticmethod
    def get_reversal_actions():
        return ButtonAction.LAST, ButtonAction.OTHER
