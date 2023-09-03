from sys import exit
from json import dumps
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from common.gui.forms.license_window import Ui_LicenseWindow
from common.gui.decorators.window_settings import set_window_icon, frameless_window
from common.lib.constants.TermFilesPath import TermFilesPath
from common.lib.data_models.License import LicenseInfo
from datetime import datetime
from logging import warning, debug
from common.lib.constants.TextConstants import TextConstants
from common.lib.exceptions.exceptions import LicenseDataLoadingError


class LicenseWindow(Ui_LicenseWindow, QDialog):
    def __init__(self):
        super(LicenseWindow, self).__init__()
        self.setupUi(self)
        self._setup()

    @frameless_window
    @set_window_icon
    def _setup(self):
        self.InfoBoard.setText(TextConstants.LICENSE_AGREEMENT)

        try:
            self.license_info: LicenseInfo = LicenseInfo.parse_file(TermFilesPath.LICENSE_INFO)
        except Exception as license_parsing_error:
            raise LicenseDataLoadingError(f"GNU license info file parsing error: {license_parsing_error}")

        self.CheckBoxAgreement.stateChanged.connect(self.block_acceptance)
        self.rejected.connect(self.reject_license)
        self.accepted.connect(self.accept_license)
        self.block_acceptance()

    def accept_license(self):
        self.license_info.accepted = bool(self.CheckBoxAgreement.checkState().value)

        if not self.license_info.accepted:
            return

        self.license_info.last_acceptance_date = datetime.utcnow()
        self.license_info.show_agreement = not bool(self.CheckBoxDontShowAgain.checkState().value)

        with open(TermFilesPath.LICENSE_INFO, 'w') as license_file:
            license_data = dict(
                accepted=self.license_info.accepted,
                show_agreement=self.license_info.show_agreement,
                last_acceptance_date=self.license_info.last_acceptance_date.isoformat(),
                license_id=self.license_info.license_id,
            )

            license_file.write(dumps(license_data, indent=4))

        debug(f"Licence agreement accepted {self.license_info.last_acceptance_date.isoformat()}")

        self.close()

    def reject_license(self):
        with open(TermFilesPath.LICENSE_INFO, 'w') as license_file:
            license_data = dict(
                accepted=False,
                show_agreement=True,
                last_acceptance_date=None,
                license_id=self.license_info.license_id,
            )

            license_file.write(dumps(license_data, indent=4))

        warning("License agreement rejected, exit")

        exit()

    def block_acceptance(self):
        accepted = bool(self.CheckBoxAgreement.checkState().value)

        if not accepted:
            self.CheckBoxDontShowAgain.setCheckState(Qt.CheckState.Unchecked)

        self.CheckBoxDontShowAgain.setEnabled(accepted)
        self.ButtonAccept.setEnabled(accepted)
