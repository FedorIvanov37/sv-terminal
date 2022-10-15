from common.app.forms.error import Ui_Error
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from common.app.constants.FilePath import FilePath


class ErrorWindow(Ui_Error, QDialog):
    def __init__(self, exception: Exception = None, error_text: str = ""):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(FilePath.MAIN_LOGO))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.accepted.connect(self.exit)
        self.rejected.connect(self.exit)
        self.show_error(exception, error_text)

    def show_error(self, exception: Exception = None, error_text: str = ""):
        text = str(exception) if exception else str()
        text += "\n" + error_text
        self.TextField.append(text)

    @staticmethod
    def exit(error_code=100):
        exit(error_code)
