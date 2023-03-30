from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from PyQt6.QtMultimedia import QMediaPlayer
from common.app.forms.about import Ui_AboutWindow
from common.app.constants.FilePath import FilePath
from common.app.constants.ReleaseDefinitoin import ReleaseDefinition


class AboutWindow(Ui_AboutWindow, QDialog):
    _player = QMediaPlayer()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(FilePath.MAIN_LOGO))
        self.logoLabel.setPixmap(QPixmap(FilePath.MAIN_LOGO))

        data_bind = {
            self.VersionLabel: ReleaseDefinition.VERSION,
            self.ReleaseLabel: ReleaseDefinition.RELEASE,
            self.ContactLabel: ReleaseDefinition.CONTACT,
            self.AuthorLabel: ReleaseDefinition.AUTHOR
        }

        for element in data_bind:
            element.setText("%s %s" % (element.text(), data_bind.get(element)))
