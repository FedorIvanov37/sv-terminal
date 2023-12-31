from logging import info, error, getLogger, getLevelName
from PyQt6.QtWidgets import QDialog, QLineEdit, QCheckBox
from PyQt6.QtGui import QRegularExpressionValidator, QIcon, QPixmap, QIntValidator
from PyQt6.QtCore import QRegularExpression
from common.lib.constants import LogDefinition, TermFilesPath
from common.lib.data_models.Config import Config
from common.gui.forms.settings import Ui_SettingsWindow
from common.gui.constants import GuiFilesPath
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
    def setup(self) -> None:
        self.ButtonAbout.setIcon(QIcon(QPixmap(GuiFilesPath.MAIN_LOGO)))
        self.SvAddress.setValidator(QRegularExpressionValidator(QRegularExpression(r"(\d+\.){1,3}\d+")))
        self.MaxAmount.setEditable(True)
        self.RemoteSpecUrl.editingFinished.connect(lambda: self.RemoteSpecUrl.setCursorPosition(int()))
        self.MaxAmount.setValidator(QIntValidator(1, 2_100_000_000, self.MaxAmount))
        self.DebugLevel.addItems(LogDefinition.LOG_LEVEL)
        self.ParseSubfields.setHidden(True)  # TODO
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)
        self.ButtonAbout.pressed.connect(self.about)
        self.HeaderLength.textChanged.connect(self.validate_header_length)
        self.DebugLevel.currentIndexChanged.connect(self.process_debug_level_change)
        self.KeepAliveMode.stateChanged.connect(lambda state: self.KeepAliveInterval.setEnabled(bool(state)))
        self.HeaderLengthMode.stateChanged.connect(lambda state: self.HeaderLength.setEnabled(bool(state)))
        self.BackupStorageCheckbox.stateChanged.connect(lambda state: self.StorageDepth.setEnabled(bool(state)))
        self.MaxAmountBox.stateChanged.connect(lambda state: self.MaxAmount.setEnabled(bool(state)))
        self.UseRemoteSpec.stateChanged.connect(self.process_spec_usage_change)
        self.ButtonDefault.clicked.connect(self.set_default_settings)
        self.LoadSpec2.stateChanged.connect(lambda: self.LoadSpec.setChecked(self.LoadSpec2.isChecked()))
        self.LoadSpec.stateChanged.connect(lambda: self.LoadSpec2.setChecked(self.LoadSpec.isChecked()))
        self.ValidationEnabled.stateChanged.connect(self.process_validation_change)
        self.ValidationMode.stateChanged.connect(self.process_validation_mode_change)
        self.process_config(self.config)
        self.process_spec_usage_change()
        self.process_validation_change()
        self.process_validation_mode_change()

    @staticmethod
    def about() -> None:
        AboutWindow()

    def process_config(self, config: Config) -> None:
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
        self.UseRemoteSpec.setChecked(config.remote_spec.use_remote_spec)
        self.RemoteSpecUrl.setText(config.remote_spec.remote_spec_url)
        self.RemoteSpecUrl.setCursorPosition(int())
        self.RewriteLocalSpec.setChecked(config.remote_spec.rewrite_local_spec)
        self.StorageDepth.setValue(config.remote_spec.backup_storage_depth)
        self.BackupStorageCheckbox.setChecked(config.remote_spec.backup_storage)
        self.LoadSpec.setChecked(config.terminal.load_remote_spec)
        self.LoadSpec2.setChecked(config.terminal.load_remote_spec)

        if not config.fields.max_amount_limited:
            return

        max_amount: str = str(config.fields.max_amount)

        if (index := self.MaxAmount.findText(max_amount)) < int():  # If the max_amount from config is not found
            index: int = int()
            self.MaxAmount.insertItem(index, max_amount)

        self.MaxAmount.setCurrentIndex(index)

    def set_default_settings(self) -> None:
        try:
            with open(TermFilesPath.DEFAULT_CONFIG) as json_file:
                default_config: Config = Config.model_validate_json(json_file.read())

        except Exception as parsing_error:
            error(parsing_error)
            return

        default_config.host.host = self.config.host.host
        default_config.host.port = self.config.host.port
        default_config.remote_spec.remote_spec_url = self.config.remote_spec.remote_spec_url
        default_config.remote_spec.rewrite_local_spec = self.config.remote_spec.rewrite_local_spec

        self.process_config(default_config)

    def validate_header_length(self) -> None:
        header_length: int = int(self.HeaderLength.value())

        if self.HeaderLengthMode.isChecked() and self.HeaderLength.value() < 2:
            self.HeaderLength.setValue(2)

        if header_length % 2 != int():
            self.HeaderLength.setValue(header_length - 1)

    def process_validation_mode_change(self):
        self.ValidationReaction.setEnabled(self.ValidationMode.isChecked())

    def process_debug_level_change(self) -> None:
        disabled: bool = False
        checked: bool = self.config.debug.clear_log

        if self.DebugLevel.currentText() == LogDefinition.DEBUG:
            checked: bool = False
            disabled: bool = True

        for checkbox in self.ClearLog, self.HideSecrets:
            checkbox.setChecked(checked)
            checkbox.setDisabled(disabled)

    def process_validation_change(self):
        elements = [
            self.ValidateIncoming,
            self.ValidationMode,
            self.ValidationReaction,
        ]

        for elements in elements:
            elements.setEnabled(self.ValidationEnabled.isChecked())

    def process_spec_usage_change(self) -> None:
        elements: set[QLineEdit | QCheckBox] = {
            self.RemoteSpecUrl,
            self.RewriteLocalSpec,
            self.BackupStorageCheckbox,
            self.LoadSpec,
            self.LoadSpec2
        }

        for element in elements:
            element.setEnabled(self.UseRemoteSpec.isChecked())

        self.LoadSpec.setText("Load remote specification")

        if not self.LoadSpec.isEnabled():
            self.LoadSpec.setText(f"{self.LoadSpec.text()} (disabled below)")

    def ok(self) -> None:
        getLogger().setLevel(getLevelName(self.DebugLevel.currentText()))

        config = self.config

        config.host.host = self.SvAddress.text()
        config.host.port = self.SvPort.value()
        config.host.keep_alive_mode = self.KeepAliveMode.isChecked()
        config.host.header_length_exists = self.HeaderLengthMode.isChecked()
        config.terminal.process_default_dump = self.ProcessDefaultDump.isChecked()
        config.terminal.connect_on_startup = self.ConnectOnStartup.isChecked()
        config.terminal.load_remote_spec = self.LoadSpec.isChecked()
        config.debug.parse_subfields = self.ParseSubfields.isChecked()
        config.fields.max_amount_limited = self.MaxAmountBox.isChecked()
        config.debug.clear_log = self.ClearLog.isChecked()
        config.host.keep_alive_interval = self.KeepAliveInterval.value()
        config.host.header_length = self.HeaderLength.value()
        config.debug.level = self.DebugLevel.currentText()
        config.fields.max_amount = int(self.MaxAmount.currentText())
        config.fields.build_fld_90 = self.BuildFld90.isChecked()
        config.fields.send_internal_id = self.SendInternalId.isChecked()
        config.fields.validation = self.ValidationEnabled.isChecked()
        config.fields.json_mode = self.JsonMode.isChecked()
        config.fields.hide_secrets = self.HideSecrets.isChecked()
        config.remote_spec.use_remote_spec = self.UseRemoteSpec.isChecked()
        config.remote_spec.remote_spec_url = self.RemoteSpecUrl.text()
        config.remote_spec.rewrite_local_spec = self.RewriteLocalSpec.isChecked()
        config.remote_spec.backup_storage = self.BackupStorageCheckbox.isChecked()
        config.remote_spec.backup_storage_depth = self.StorageDepth.value()

        if not config.fields.max_amount_limited:
            config.fields.max_amount = 9_999_999_999

        with open(TermFilesPath.CONFIG, "w") as file:
            file.write(self.config.model_dump_json(indent=4))

        self.accept()

    def cancel(self) -> None:
        info("Settings applying was canceled")
        self.reject()
