from json import dumps
from common.gui.forms.settings import Ui_SettingsWindow
from common.gui.constants.TermFilesPath import TermFilesPath
from common.gui.forms.help_window import Croak
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator, QIcon, QPixmap
from PyQt6.QtCore import Qt, QRegularExpression
from common.gui.constants.TextConstants import TextConstants
from common.gui.constants.LogDefinition import LogDefinition
from logging import info, warning, getLogger, getLevelName
from common.gui.windows.about_window import AboutWindow
from common.lib.data_models.Config import Config


class SettingsWindow(Ui_SettingsWindow, QDialog):
    def __init__(self, config: Config):
        super().__init__()
        self.setupUi(self)
        self.config: Config = config
        self.setup()

    def setup(self):
        self.setWindowIcon(QIcon(TermFilesPath.MAIN_LOGO))
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        self.ButtonAbout.setIcon(QIcon(QPixmap(TermFilesPath.MAIN_LOGO)))
        self.SvPort.setValidator(QIntValidator(1, 65535))
        self.SvAddress.setValidator(QRegularExpressionValidator(QRegularExpression(r"(\d+\.){3}\d+")))
        self.MaxAmount.setValidator(QRegularExpressionValidator(QRegularExpression(r"\d{1,12}|" + self.easter)))
        self.DebugLevel.addItems(LogDefinition.LOG_LEVEL)
        self.ParseSubfields.setHidden(True)  # TODO
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)
        self.ButtonAbout.pressed.connect(self.about)
        self.DebugLevel.currentIndexChanged.connect(self.process_debug_level_change)
        self.process_config()

    @staticmethod
    def about():
        AboutWindow().exec()

    def process_config(self):
        self.DebugLevel.setCurrentText(self.config.debug.level)
        self.SvAddress.setText(self.config.smartvista.host)
        self.SvPort.setText(self.config.smartvista.port)
        self.MaxAmount.setText(str(self.config.fields.max_amount))
        self.MaxAmount.textEdited.connect(self.croak)
        self.ProcessDefaultDump.setChecked(self.config.terminal.process_default_dump)
        self.ConnectOnStartup.setChecked(self.config.terminal.connect_on_startup)
        self.ClearLog.setChecked(self.config.debug.clear_log)
        self.ParseSubfields.setChecked(self.config.debug.parse_subfields)
        self.BuildFld90.setChecked(self.config.fields.build_fld_90)
        self.SendInternalId.setChecked(self.config.fields.send_internal_id)
        self.ValidationEnabled.setChecked(self.config.fields.validation)

    def process_debug_level_change(self, _):
        disabled = False
        checked = bool(self.ClearLog.checkState())

        if self.DebugLevel.currentText() == LogDefinition.DEBUG:
            checked = False
            disabled = True

        self.ClearLog.setChecked(checked)
        self.ClearLog.setDisabled(disabled)

    def ok(self):
        getLogger().setLevel(getLevelName(self.DebugLevel.currentText()))

        if not self.MaxAmount.text().isdigit():  # croak
            self.MaxAmount.setText("100")

        self.MaxAmount.setText(str(int(self.MaxAmount.text())))
        self.config.smartvista.host = self.SvAddress.text()
        self.config.smartvista.port = self.SvPort.text()
        self.config.terminal.process_default_dump = self.ProcessDefaultDump.isChecked()
        self.config.terminal.connect_on_startup = self.ConnectOnStartup.isChecked()
        self.config.debug.clear_log = self.ClearLog.isChecked()
        self.config.debug.level = self.DebugLevel.currentText()
        self.config.debug.parse_subfields = self.ParseSubfields.isChecked()
        self.config.fields.max_amount = self.MaxAmount.text()
        self.config.fields.build_fld_90 = self.BuildFld90.isChecked()
        self.config.fields.send_internal_id = self.SendInternalId.isChecked()
        self.config.fields.validation = self.ValidationEnabled.isChecked()

        with open(TermFilesPath.CONFIG, "w") as file:
            file.write(dumps(self.config.dict(), indent=4))

        info("Settings applied")

        if "" in (self.SvAddress.text(), self.SvPort.text()):
            warning("Lost SV address or SV port! Check the parameters.")

        self.accepted.emit()
        self.close()

    def cancel(self):
        info("Settings applying was canceled")
        self.close()

    def croak(self):
        if self.MaxAmount.text() != self.easter:
            return

        self.MaxAmount.setText(Croak().max_amount)

    easter = "".join(map(chr, TextConstants.EASTER))
