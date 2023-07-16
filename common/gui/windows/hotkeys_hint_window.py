from common.gui.forms.hotkeys import Ui_HotKeysHint
from common.gui.constants.TermFilesPath import TermFilesPath
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class HotKeysHintWindow(Ui_HotKeysHint, QDialog):
    def __init__(self):
        super(HotKeysHintWindow, self).__init__()
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.setWindowIcon(QIcon(TermFilesPath.MAIN_LOGO))
        header = self.HintTable.horizontalHeader()
        header.setSectionResizeMode(header.ResizeMode.Fixed)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.HintTable.setColumnWidth(0, 200)
        self.HintTable.setColumnWidth(1, 400)
        self.exec()
