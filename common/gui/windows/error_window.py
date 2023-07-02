from traceback import format_exc
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from common.gui.forms.error import Ui_Error
from common.gui.constants.TermFilesPath import TermFilesPath


class ErrorWindow(Ui_Error, QDialog):
    def __init__(self, exc):
        super().__init__()

        self.exception = exc

        try:
            self.setupUi(self)
            self.setWindowIcon(QIcon(TermFilesPath.MAIN_LOGO))
            self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
            self.accepted.connect(self.exit)
            self.rejected.connect(self.exit)
            self.TextField.append(format_exc())

        except Exception as exc:
            self.exit(exc)

    def exit(self, exception=None, error_code=100):
        print(f"Finished with error: {exception if exception else self.exception}")
        exit(error_code)
