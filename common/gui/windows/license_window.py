from sys import exit
from json import dump, load
from json.decoder import JSONDecodeError
from logging import warning, info
from pydantic import ValidationError
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from common.gui.forms.license_window import Ui_LicenseWindow
from common.gui.decorators.window_settings import set_window_icon, frameless_window
from common.lib.constants import TermFilesPath, TextConstants
from common.lib.data_models.License import LicenseInfo
from common.lib.exceptions.exceptions import LicenseDataLoadingError, LicenceAlreadyAccepted


class LicenseWindow(Ui_LicenseWindow, QDialog):
    def __init__(self):
        super(LicenseWindow, self).__init__()
        self.setupUi(self)
        self._setup()

    @frameless_window
    @set_window_icon
    def _setup(self):
        self.LogoContainer.setText(f"{TextConstants.HELLO_MESSAGE} | GNU/GPL license agreement\n")
        self.InfoBoard.setText(TextConstants.LICENSE_AGREEMENT)
        self.CheckBoxAgreement.setFocus()

        try:
            with open(TermFilesPath.LICENSE_INFO) as json_file:
                self.license_info: LicenseInfo = LicenseInfo.model_validate(load(json_file))

        except (ValueError, ValidationError, JSONDecodeError, FileNotFoundError):
            self.license_info: LicenseInfo = LicenseInfo()

        except Exception as license_parsing_error:
            raise LicenseDataLoadingError(f"GNU license info file parsing error: {license_parsing_error}")

        if self.license_info.accepted and not self.license_info.show_agreement:
            self.print_acceptance_info()
            raise LicenceAlreadyAccepted

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

        license_data: LicenseInfo = self.license_info.model_copy(deep=True)
        license_data.last_acceptance_date = license_data.last_acceptance_date.isoformat()

        self.save_license_file(license_data)
        self.print_acceptance_info()

    def reject_license(self):
        license_data: LicenseInfo = self.license_info.model_copy(deep=True)
        license_data.accepted = False
        license_data.show_agreement = True
        license_data.last_acceptance_date = None

        self.save_license_file(license_data)
        warning("License agreement rejected, exit")
        exit(100)

    @staticmethod
    def save_license_file(license_data: LicenseInfo):
        with open(TermFilesPath.LICENSE_INFO, 'w') as license_file:
            dump(license_data.model_dump(), license_file, indent=4)

    def block_acceptance(self):
        accepted = bool(self.CheckBoxAgreement.checkState().value)

        if not accepted:
            self.CheckBoxDontShowAgain.setCheckState(Qt.CheckState.Unchecked)

        self.CheckBoxDontShowAgain.setEnabled(accepted)
        self.ButtonAccept.setEnabled(accepted)

    def print_acceptance_info(self):
        info(f"Licence agreement accepted {self.license_info.last_acceptance_date}")
        info(f"License ID {self.license_info.license_id}")
        info(f"Thank you for using SIGNAL")
