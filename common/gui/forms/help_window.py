from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMovie, QIcon, QKeyEvent
from PyQt6.QtWidgets import QDialog
from common.gui.forms.help import Ui_HelpWindow
from common.gui.constants.FilePath import FilePath


# All glory to the Hypnotoad!


class Croak(Ui_HelpWindow, QDialog):
    _max_amount = "100"

    @property
    def max_amount(self):
        return self._max_amount

    def __init__(self):
        try:
            super().__init__()
            self.setupUi(self)
            self.movie = QMovie(r"common\app\forms\help.pyc")
            self.setWindowIcon(QIcon(FilePath.MAIN_LOGO))
            self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
            self.Toad.setMovie(self.movie)
            self.movie.start()
            self.show()
            self.exec()

        except Exception:
            ...

    def keyPressEvent(self, a0: QKeyEvent) -> None:  # TODO does not work :(
        if a0.key() == Qt.Key.Key_Escape:
            self.close()  # WTF
