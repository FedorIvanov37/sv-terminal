from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from common.gui.forms.about import Ui_AboutWindow
from common.gui.constants.TermFilesPath import TermFilesPath
from common.gui.constants.ReleaseDefinitoin import ReleaseDefinition
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from os import getcwd, path
from PyQt6.QtGui import QCloseEvent, QKeyEvent


class AboutWindow(Ui_AboutWindow, QDialog):
    player = QMediaPlayer()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()
        self.play()

    def setup(self):
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(TermFilesPath.MAIN_LOGO))
        self.logoLabel.setPixmap(QPixmap(TermFilesPath.MAIN_LOGO))
        self.MusicOnOfButton.setIcon(QIcon(QPixmap(TermFilesPath.MAIN_LOGO)))
        self.MusicOnOfButton.clicked.connect(self.switch_musing)
        self.MusicOnOfButton.setIcon(QIcon(QPixmap(TermFilesPath.MUSIC_ON)))

        data_bind = {
            self.VersionLabel: ReleaseDefinition.VERSION,
            self.ReleaseLabel: ReleaseDefinition.RELEASE,
            self.ContactLabel: ReleaseDefinition.CONTACT,
            self.AuthorLabel: ReleaseDefinition.AUTHOR
        }

        for element in data_bind:
            element.setText("%s %s" % (element.text(), data_bind.get(element)))

    def play(self):
        music_file_path = path.normpath(f"{getcwd()}/{TermFilesPath.VVVVVV}")
        music_file_path = QUrl.fromLocalFile(music_file_path)
        audio_output = QAudioOutput()
        self.player.setAudioOutput(audio_output)
        self.player.setSource(music_file_path)
        self.exec()

    def switch_musing(self):
        icon = None

        match self.player.playbackState():
            case self.player.PlaybackState.PlayingState:
                icon = TermFilesPath.MUSIC_ON
                self.player.stop()

            case self.player.PlaybackState.StoppedState:
                icon = TermFilesPath.MUSIC_OFF
                self.player.play()

            case self.player.PlaybackState.PausedState:
                icon = TermFilesPath.MUSIC_OFF
                self.player.stop()
                self.player.play()

        self.MusicOnOfButton.setIcon(QIcon(QPixmap(icon)))

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.player.stop()
        a0.accept()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()
