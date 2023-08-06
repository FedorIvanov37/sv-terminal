from dataclasses import dataclass


@dataclass(frozen=True)
class KeySequence:
    CTRL_T = 'Ctrl+T'
    CTRL_R = 'Ctrl+R'
    CTRL_L = 'Ctrl+L'
    CTRL_E = 'Ctrl+E'
    CTRL_W = 'Ctrl+W'
    CTRL_ALT_Q = 'Ctrl+Alt+Q'
    CTRL_ENTER = 'Ctrl+Return'
    CTRL_SHIFT_ENTER = 'Ctrl+Shift+Return'
    CTRL_SHIFT_N = 'Ctrl+Shift+N'
    CTRL_ALT_ENTER = 'Ctrl+Alt+Return'
