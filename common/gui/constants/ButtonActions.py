from dataclasses import dataclass


@dataclass
class ButtonAction(object):
    LAST = "Last"
    OTHER = "Other"
    BUTTON_PLUS_SIGN = "✚"
    BUTTON_MINUS_SIGN = "━"
    BUTTON_NEXT_LEVEL_SIGN = "🡾"

    @staticmethod
    def get_reversal_actions():
        return ButtonAction.LAST, ButtonAction.OTHER
