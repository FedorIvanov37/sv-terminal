from os import getcwd, path
from PyQt6.QtGui import QPixmap, QIcon, QDesktopServices, QCloseEvent, QKeyEvent
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QDialog
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from common.gui.forms.about import Ui_AboutWindow
from common.gui.constants.TermFilesPath import TermFilesPath
from common.gui.constants.ReleaseDefinitoin import ReleaseDefinition


class AboutWindow(Ui_AboutWindow, QDialog):
    player = QMediaPlayer()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()
        self.init_music_player()

    def setup(self):
        self.setWindowIcon(QIcon(TermFilesPath.MAIN_LOGO))
        self.logoLabel.setPixmap(QPixmap(TermFilesPath.MAIN_LOGO))
        self.MusicOnOfButton.setIcon(QIcon(QPixmap(TermFilesPath.MAIN_LOGO)))
        self.MusicOnOfButton.clicked.connect(self.switch_musing)
        self.MusicOnOfButton.setIcon(QIcon(QPixmap(TermFilesPath.MUSIC_ON)))
        self.ContactLabel.linkActivated.connect(self.open_url)
        # self.ContactLabel.linkActivated.connect(self.play_music)

        data_bind = {
            self.VersionLabel: ReleaseDefinition.VERSION,
            self.ReleaseLabel: ReleaseDefinition.RELEASE,
            self.ContactLabel: ReleaseDefinition.CONTACT,
            self.AuthorLabel: ReleaseDefinition.AUTHOR
        }

        for element in data_bind:
            element.setText("%s %s" % (element.text(), data_bind.get(element)))

    def init_music_player(self):
        music_file_path = path.normpath(f"{getcwd()}/{TermFilesPath.VVVVVV}")
        music_file_path = QUrl.fromLocalFile(music_file_path)
        audio_output = QAudioOutput()
        self.player.setAudioOutput(audio_output)
        self.player.setSource(music_file_path)
        self.exec()

    def play_music(self):
        if self.player.playbackState() == self.player.PlaybackState.PlayingState:
            return

        self.player.play()
        self.MusicOnOfButton.setIcon(QIcon(QPixmap(TermFilesPath.MUSIC_OFF)))

    def switch_musing(self):
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

            case _:
                return

        self.MusicOnOfButton.setIcon(QIcon(QPixmap(icon)))

    @staticmethod
    def open_url(link):
        link = QUrl(link)
        QDesktopServices.openUrl(link)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.player.stop()
        a0.accept()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()
