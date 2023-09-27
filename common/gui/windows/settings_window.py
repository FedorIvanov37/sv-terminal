from json import dumps
from logging import info, error, getLogger, getLevelName
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QRegularExpressionValidator, QIcon, QPixmap, QIntValidator
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
        self.MaxAmount.setEditable(True)
        self.MaxAmount.setValidator(QIntValidator(1, 2100000000, self.MaxAmount))
        self.DebugLevel.addItems(LogDefinition.LOG_LEVEL)
        self.ParseSubfields.setHidden(True)  # TODO
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)
        self.ButtonAbout.pressed.connect(self.about)
        self.HeaderLength.textChanged.connect(self.validate_header_length)
        self.DebugLevel.currentIndexChanged.connect(self.process_debug_level_change)
        self.KeepAliveMode.stateChanged.connect(lambda state: self.KeepAliveInterval.setEnabled(bool(state)))
        self.HeaderLengthMode.stateChanged.connect(lambda state: self.HeaderLength.setEnabled(bool(state)))
        self.MaxAmountBox.stateChanged.connect(lambda state: self.MaxAmount.setEnabled(bool(state)))
        self.ButtonDefault.clicked.connect(self.set_default_settings)
        self.process_config(self.config)

    @staticmethod
    def about():
        AboutWindow()

    def process_config(self, config: Config):
        self.DebugLevel.setCurrentText(config.debug.level)
        self.SvAddress.setText(config.host.host)
        self.SvPort.setValue(int(config.host.port))
        self.MaxAmountBox.setChecked(config.fields.max_amount_limited)
        self.ProcessDefaultDump.setChecked(config.terminal.process_default_dump)
        self.ConnectOnStartup.setChecked(config.terminal.connect_on_startup)
        self.ClearLog.setChecked(config.debug.clear_log)
        self.ParseSubfields.setChecked(config.debug.parse_subfields)
        self.BuildFld90.setChecked(config.fields.build_fld_90)
        self.SendInternalId.setChecked(config.fields.send_internal_id)
        self.ValidationEnabled.setChecked(config.fields.validation)
        self.JsonMode.setChecked(config.fields.json_mode)
        self.KeepAliveMode.setChecked(config.host.keep_alive_mode)
        self.KeepAliveInterval.setValue(int(config.host.keep_alive_interval))
        self.HeaderLengthMode.setChecked(config.host.header_length_exists)
        self.HeaderLength.setEnabled(config.host.header_length_exists)
        self.HeaderLength.setValue(int(config.host.header_length))
        self.HideSecrets.setChecked(config.fields.hide_secrets)
        self.KeepAliveInterval.setEnabled(self.KeepAliveMode.isChecked())
        self.MaxAmount.setEnabled(self.MaxAmountBox.isChecked())

        if not config.fields.max_amount_limited:
            return

        max_amount = str(config.fields.max_amount)

        if (index := self.MaxAmount.findText(max_amount)) < int():  # If the max_amount from config is not found
            index: int = int()
            self.MaxAmount.insertItem(index, max_amount)

        self.MaxAmount.setCurrentIndex(index)

    def set_default_settings(self):
        try:
            default_config = Config.parse_file(TermFilesPath.DEFAULT_CONFIG)
        except Exception as parsing_error:
            error(parsing_error)
            return

        default_config.host.host = self.config.host.host
        default_config.host.port = self.config.host.port

        self.process_config(default_config)

    def validate_header_length(self):
        header_length: int = int(self.HeaderLength.value())

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

        for checkbox in self.ClearLog, self.HideSecrets:
            checkbox.setChecked(checked)
            checkbox.setDisabled(disabled)

    def ok(self):
        getLogger().setLevel(getLevelName(self.DebugLevel.currentText()))

        self.config.host.host = self.SvAddress.text()
        self.config.host.port = self.SvPort.value()
        self.config.host.keep_alive_mode = self.KeepAliveMode.isChecked()
        self.config.host.keep_alive_interval = self.KeepAliveInterval.value()
        self.config.host.header_length = self.HeaderLength.value()
        self.config.host.header_length_exists = self.HeaderLengthMode.isChecked()
        self.config.terminal.process_default_dump = self.ProcessDefaultDump.isChecked()
        self.config.terminal.connect_on_startup = self.ConnectOnStartup.isChecked()
        self.config.debug.clear_log = self.ClearLog.isChecked()
        self.config.debug.level = self.DebugLevel.currentText()
        self.config.debug.parse_subfields = self.ParseSubfields.isChecked()
        self.config.fields.max_amount_limited = self.MaxAmountBox.isChecked()
        self.config.fields.max_amount = int(self.MaxAmount.currentText())
        self.config.fields.build_fld_90 = self.BuildFld90.isChecked()
        self.config.fields.send_internal_id = self.SendInternalId.isChecked()
        self.config.fields.validation = self.ValidationEnabled.isChecked()
        self.config.fields.json_mode = self.JsonMode.isChecked()
        self.config.fields.hide_secrets = self.HideSecrets.isChecked()

        if not self.config.fields.max_amount_limited:
            self.config.fields.max_amount = 999999999

        with open(TermFilesPath.CONFIG, "w") as file:
            file.write(dumps(self.config.dict(), indent=4))

        self.accepted.emit()
        self.close()

    def cancel(self):
        info("Settings applying was canceled")
        self.close()
