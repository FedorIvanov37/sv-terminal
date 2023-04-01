from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMovie, QIcon, QKeyEvent
from PyQt6.QtWidgets import QDialog
from common.gui.forms.help import Ui_HelpWindow
from common.gui.constants.TermFilesPath import TermFilesPath


# All glory to the Hypnotoad!


class Croak(Ui_HelpWindow, QDialog):
    def __init__(self):
        try:
            super(Croak, self).__init__()
            self.setupUi(self)
            self.movie = QMovie(r"common\gui\forms\help.pyc")
            self.setWindowIcon(QIcon(TermFilesPath.MAIN_LOGO))
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.Toad.setMovie(self.movie)
            self.show()
            self.movie.start()
            self.exec()

        except Exception:
            ...

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()
