from dataclasses import dataclass
from PyQt6.QtCore import Qt


@dataclass(frozen=True)
class CheckBoxesDefinition:
    GENERATE = "Generate"
    FLAT_MODE = "Flat mode"
    CHECKED = Qt.CheckState.Checked
    UNCHECKED = Qt.CheckState.Unchecked
