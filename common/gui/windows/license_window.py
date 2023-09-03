from sys import exit
from json import dumps
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from common.lib.data_models.Config import Config
from common.gui.forms.license_window import Ui_LicenseWindow
from common.gui.decorators.window_settings import set_window_icon, frameless_window
from common.lib.constants.TermFilesPath import TermFilesPath


class LicenseWindow(Ui_LicenseWindow, QDialog):
    def __init__(self, config: Config):
        super(LicenseWindow, self).__init__()
        self.config = config
        self.setupUi(self)
        self.setup()

    @frameless_window
    @set_window_icon
    def setup(self):
        self.block_acceptance()
        self.CheckBoxAgreement.stateChanged.connect(self.block_acceptance)
        self.rejected.connect(exit)
        self.accepted.connect(self.accept_license)
        self.accepted.connect(self.close)

    def accept_license(self):
        self.config.license.accepted = bool(self.CheckBoxDontShowAgain.checkState().value)

        with open(TermFilesPath.CONFIG, 'w') as config_file:
            config_file.write(dumps(self.config.dict(), indent=4))

    def block_acceptance(self):
        accepted = bool(self.CheckBoxAgreement.checkState().value)

        if not accepted:
            self.CheckBoxDontShowAgain.setCheckState(Qt.CheckState.Unchecked)

        self.CheckBoxDontShowAgain.setEnabled(accepted)
        self.ButtonAccept.setEnabled(accepted)
