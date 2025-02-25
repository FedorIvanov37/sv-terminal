from common.gui.forms.about import Ui_AboutWindow
from common.gui.enums.GuiFilesPath import GuiFilesPath
from common.lib.enums.ReleaseDefinition import ReleaseDefinition
from common.gui.decorators.window_settings import frameless_window
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import (
    QPixmap,
    QIcon,
    QDesktopServices,
    QCloseEvent,
    QKeyEvent,
    QMovie,
)


class AboutWindow(Ui_AboutWindow, QDialog):
    audio_output = QAudioOutput()
    player = QMediaPlayer()
    movie: QMovie

    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setupUi(self)
        self.setup()

    @frameless_window
    def setup(self):
        self.logoLabel.setPixmap(QPixmap(GuiFilesPath.SIGNED_LOGO))
        self.MusicOnOfButton.setIcon(QIcon(QPixmap(GuiFilesPath.MAIN_LOGO)))
        self.MusicOnOfButton.clicked.connect(self.switch_music)
        self.MusicOnOfButton.setIcon(QIcon(QPixmap(GuiFilesPath.MUSIC_ON)))
        self.ContactLabel.linkActivated.connect(self.open_url)

        data_bind = {
            self.VersionLabel: ReleaseDefinition.VERSION,
            self.ReleaseLabel: ReleaseDefinition.RELEASE,
            self.ContactLabel: ReleaseDefinition.CONTACT,
            self.AuthorLabel: ReleaseDefinition.AUTHOR,
        }

        for label, text in data_bind.items():
            label.setText(f"{label.text()} {text}")

        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(GuiFilesPath.VVVVVV))
        self.player.playbackStateChanged.connect(self.record_finished)

    @staticmethod
    def open_url(link):
        link = QUrl(link)
        QDesktopServices.openUrl(link)

    def record_finished(self, state):
        if state == self.player.PlaybackState.StoppedState:
            self.MusicOnOfButton.setIcon(QIcon(QPixmap(GuiFilesPath.MUSIC_ON)))

    def switch_music(self):
        match self.player.playbackState():
            case self.player.PlaybackState.StoppedState:
                icon = GuiFilesPath.MUSIC_OFF
                self.player.play()

            case self.player.PlaybackState.PlayingState:
                icon = GuiFilesPath.MUSIC_ON
                self.player.stop()

            case _:
                return

        self.MusicOnOfButton.setIcon(QIcon(QPixmap(icon)))

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.player.stop()
        a0.accept()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()
