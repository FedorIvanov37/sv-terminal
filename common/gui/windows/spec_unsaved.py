from common.gui.forms.spec_unsaved import Ui_SpecUnsaved
from PyQt6.QtWidgets import QDialog, QMenu
from PyQt6.QtGui import QIcon, QCloseEvent, QKeyEvent, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from common.gui.constants.TermFilesPath import TermFilesPath


class SpecUnsaved(Ui_SpecUnsaved, QDialog):
    _save: pyqtSignal = pyqtSignal(bool)
    _return_to_spec: pyqtSignal = pyqtSignal()

    @property
    def return_to_spec(self):
        return self._return_to_spec

    @property
    def save(self):
        return self._save

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(TermFilesPath.MAIN_LOGO))
        self.setup()

    def setup(self):
        apply_menu = QMenu()

        for action in ("For current session", "Permanently"):
            apply_menu.addAction(action, self.need_apply)

        self.ButtonSave.setMenu(apply_menu)
        self.ButtonReturn.clicked.connect(self.return_to_spec.emit)

    def need_apply(self):
        commit = self.sender().text().upper() == "PERMANENTLY"  # TODO Hardcode
        self.save.emit(commit)
        self.accept()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.return_to_spec.emit()
        a0.accept()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()
