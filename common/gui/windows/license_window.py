from sys import exit
from json.decoder import JSONDecodeError
from logging import warning, info
from pydantic import ValidationError
from datetime import datetime, UTC
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QPixmap
from common.gui.forms.license_window import Ui_LicenseWindow
from common.gui.decorators.window_settings import set_window_icon, frameless_window
from common.lib.data_models.License import LicenseInfo
from common.lib.exceptions.exceptions import LicenseDataLoadingError, LicenceAlreadyAccepted
from common.lib.enums.TermFilesPath import TermFilesPath
from common.gui.enums.GuiFilesPath import GuiFilesPath
from common.lib.enums.TextConstants import TextConstants


class LicenseWindow(Ui_LicenseWindow, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._setup()

    @frameless_window
    @set_window_icon
    def _setup(self):
        self.LogoLabel.setPixmap(QPixmap(GuiFilesPath.SIGNED_LOGO))
        self.InfoBoard.setText(TextConstants.LICENSE_AGREEMENT)
        self.CheckBoxAgreement.setFocus()

        try:
            with open(TermFilesPath.LICENSE_INFO) as json_file:
                self.license_info: LicenseInfo = LicenseInfo.model_validate_json(json_file.read())

        except (ValueError, ValidationError, JSONDecodeError, FileNotFoundError):
            self.license_info: LicenseInfo = LicenseInfo()

        except Exception as license_parsing_error:
            raise LicenseDataLoadingError(f"GNU license info file parsing error: {license_parsing_error}")

        if self.license_info.accepted and not self.license_info.show_agreement:
            self.print_acceptance_info()
            raise LicenceAlreadyAccepted

        self.CheckBoxAgreement.setChecked(self.license_info.accepted)
        self.CheckBoxAgreement.stateChanged.connect(self.block_acceptance)
        self.rejected.connect(self.reject_license)
        self.accepted.connect(self.accept_license)
        self.block_acceptance()

    def accept_license(self):
        self.license_info.accepted = bool(self.CheckBoxAgreement.checkState().value)

        if not self.license_info.accepted:
            return

        self.license_info.last_acceptance_date = datetime.now(UTC)
        self.license_info.show_agreement = not bool(self.CheckBoxDontShowAgain.checkState().value)

        license_data: LicenseInfo = self.license_info.model_copy(deep=True)
        license_data.last_acceptance_date = license_data.last_acceptance_date.isoformat()

        self.save_license_file(license_data)
        self.print_acceptance_info()
        self.close()

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
            license_file.write(license_data.model_dump_json(indent=4))

    def block_acceptance(self):
        accepted = bool(self.CheckBoxAgreement.checkState().value)

        if not accepted:
            self.CheckBoxDontShowAgain.setCheckState(Qt.CheckState.Unchecked)

        self.CheckBoxDontShowAgain.setEnabled(accepted)
        self.ButtonAccept.setEnabled(accepted)

    def print_acceptance_info(self):
        date_format = "%d/%m/%Y %T UTC"

        info(f"License ID {self.license_info.license_id} | Accepted {
            datetime.strftime(self.license_info.last_acceptance_date, date_format)}")
