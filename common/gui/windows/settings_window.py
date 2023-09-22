from json import dumps
from logging import info, warning, error, getLogger, getLevelName
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QRegularExpressionValidator, QIcon, QPixmap
from PyQt6.QtCore import QRegularExpression
from common.lib.constants.LogDefinition import LogDefinition
from common.lib.data_models.Config import Config
from common.lib.constants.TermFilesPath import TermFilesPath
from common.gui.forms.settings import Ui_SettingsWindow
from common.gui.constants.GuiFilesPath import GuiFilesPath
from common.gui.windows.about_window import AboutWindow
from common.gui.decorators.window_settings import set_window_icon, has_close_button_only


class SettingsWindow(Ui_SettingsWindow, QDialog):
    def __init__(self, config: Config):
        super(SettingsWindow, self).__init__()
        self.setupUi(self)
        self.config: Config = config
        self.setup()

    @set_window_icon
    @has_close_button_only
    def setup(self):
        self.ButtonAbout.setIcon(QIcon(QPixmap(GuiFilesPath.MAIN_LOGO)))
        self.SvAddress.setValidator(QRegularExpressionValidator(QRegularExpression(r"(\d+\.){1,3}\d+")))
        self.MaxAmount.setValidator(QRegularExpressionValidator(QRegularExpression(r"[^0|\D]\d+")))
        self.DebugLevel.addItems(LogDefinition.LOG_LEVEL)
        self.ParseSubfields.setHidden(True)  # TODO
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)
        self.ButtonAbout.pressed.connect(self.about)
        self.HeaderLength.textChanged.connect(self.validate_header_length)
        self.HeaderLengthMode.stateChanged.connect(lambda: self.HeaderLength.setValue(2 if self.HeaderLengthMode.isChecked() else int()))
        self.DebugLevel.currentIndexChanged.connect(self.process_debug_level_change)
        self.KeepAliveMode.stateChanged.connect(lambda state: self.KeepAliveInterval.setEnabled(bool(state)))
        self.HeaderLengthMode.stateChanged.connect(lambda state: self.HeaderLength.setEnabled(bool(state)))
        self.process_config()

    @staticmethod
    def about():
        AboutWindow()

    def process_config(self):
        self.DebugLevel.setCurrentText(self.config.debug.level)
        self.SvAddress.setText(self.config.host.host)
        self.SvPort.setValue(int(self.config.host.port))
        self.MaxAmount.setText(str(self.config.fields.max_amount))
        self.ProcessDefaultDump.setChecked(self.config.terminal.process_default_dump)
        self.ConnectOnStartup.setChecked(self.config.terminal.connect_on_startup)
        self.ClearLog.setChecked(self.config.debug.clear_log)
        self.ParseSubfields.setChecked(self.config.debug.parse_subfields)
        self.BuildFld90.setChecked(self.config.fields.build_fld_90)
        self.SendInternalId.setChecked(self.config.fields.send_internal_id)
        self.ValidationEnabled.setChecked(self.config.fields.validation)
        self.JsonMode.setChecked(self.config.fields.json_mode)
        self.KeepAliveMode.setChecked(self.config.host.keep_alive_mode)
        self.KeepAliveInterval.setValue(int(self.config.host.keep_alive_interval))
        self.KeepAliveInterval.setEnabled(self.KeepAliveMode.isChecked())
        self.HeaderLengthMode.setChecked(self.config.host.header_length_exists)
        self.HeaderLength.setEnabled(self.config.host.header_length_exists)
        self.HeaderLength.setValue(int(self.config.host.header_length))
        self.HideSecrets.setChecked(self.config.fields.hide_secrets)

    def validate_header_length(self):
        header_length: int = int(self.HeaderLength.text())

        if self.HeaderLengthMode.isChecked() and self.HeaderLength.value() < 2:
            self.HeaderLength.setValue(2)

        if header_length % 2 != int():
            self.HeaderLength.setValue(header_length - 1)

    def process_debug_level_change(self):
        disabled = False
        checked = self.config.debug.clear_log

        if self.DebugLevel.currentText() == LogDefinition.DEBUG:
            checked = False
            disabled = True

        self.ClearLog.setChecked(checked)
        self.ClearLog.setDisabled(disabled)

    def ok(self):
        getLogger().setLevel(getLevelName(self.DebugLevel.currentText()))

        try:  # Raise ValueError when max_amount is less than one or has a non-int value
            if int(self.MaxAmount.text()) < 1:
                raise ValueError
        except ValueError:
            warning(f"Incorrect max amount. Set the default value of 100 instead")
            self.MaxAmount.setText("100")  # When max_amount is less than one or has a non-int value

        try:
            int(self.KeepAliveInterval.text())
        except ValueError:
            error("Empty Keep Alive Interval, set default value 300 sec")
            self.KeepAliveInterval.setText("300")

        self.config.host.host = self.SvAddress.text()
        self.config.host.port = self.SvPort.text()
        self.config.host.keep_alive_mode = self.KeepAliveMode.isChecked()
        self.config.host.keep_alive_interval = self.KeepAliveInterval.text()
        self.config.host.header_length = self.HeaderLength.text()
        self.config.host.header_length_exists = self.HeaderLengthMode.isChecked()
        self.config.terminal.process_default_dump = self.ProcessDefaultDump.isChecked()
        self.config.terminal.connect_on_startup = self.ConnectOnStartup.isChecked()
        self.config.debug.clear_log = self.ClearLog.isChecked()
        self.config.debug.level = self.DebugLevel.currentText()
        self.config.debug.parse_subfields = self.ParseSubfields.isChecked()
        self.config.fields.max_amount = self.MaxAmount.text()
        self.config.fields.build_fld_90 = self.BuildFld90.isChecked()
        self.config.fields.send_internal_id = self.SendInternalId.isChecked()
        self.config.fields.validation = self.ValidationEnabled.isChecked()
        self.config.fields.json_mode = self.JsonMode.isChecked()
        self.config.fields.hide_secrets = self.HideSecrets.isChecked()

        with open(TermFilesPath.CONFIG, "w") as file:
            file.write(dumps(self.config.dict(), indent=4))

        self.accepted.emit()
        self.close()

    def cancel(self):
        info("Settings applying was canceled")
        self.close()
