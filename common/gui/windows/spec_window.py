from logging import error, info
from copy import deepcopy
from typing import Optional
from pydantic import ValidationError
from PyQt6.QtGui import QCloseEvent, QKeyEvent, QKeySequence, QShortcut
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QMenu, QDialog, QPushButton, QApplication
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.EpaySpecificationModel import EpaySpecModel, IsoField
from common.lib.data_models.Config import Config
from common.lib.constants import TermFilesPath
from common.lib.constants import TextConstants
from common.lib.core.Logger import LogStream, getLogger, Formatter
from common.lib.constants import LogDefinition
from common.lib.core.SpecFilesRotator import SpecFilesRotator
from common.gui.windows.spec_unsaved import SpecUnsaved
from common.gui.forms.spec import Ui_SpecificationWindow
from common.gui.core.json_views.SpecView import SpecView
from common.gui.windows.mti_spec_window import MtiSpecWindow
from common.gui.constants import ButtonActions, SpecFieldDef, KeySequence
from common.gui.decorators.window_settings import set_window_icon, has_close_button_only
from common.gui.core.WirelessHandler import WirelessHandler
from common.gui.windows.field_validator_window import FieldDataSet
from common.gui.core.json_items import SpecItem


class SpecWindow(Ui_SpecificationWindow, QDialog):
    _read_only: bool = True
    _spec: EpaySpecification = EpaySpecification()
    _spec_accepted: pyqtSignal = pyqtSignal(str)
    _spec_rejected: pyqtSignal = pyqtSignal()
    _reset_spec: pyqtSignal = pyqtSignal(str)
    _load_remote_spec: pyqtSignal = pyqtSignal(bool)
    _clean_spec: EpaySpecModel = None
    wireless_handler: WirelessHandler

    @property
    def load_remote_spec(self):
        return self._load_remote_spec

    @property
    def reset_spec(self):
        return self._reset_spec

    @property
    def spec_accepted(self):
        return self._spec_accepted

    @property
    def spec_rejected(self):
        return self._spec_rejected

    @property
    def spec(self):
        return self._spec

    @property
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, checked):
        self._read_only = checked

    def __init__(self, connector, config: Config):
        super(SpecWindow, self).__init__()
        self.connector = connector
        self.config = config
        self.setupUi(self)
        self._setup()

    @set_window_icon
    @has_close_button_only
    def _setup(self):
        self.SpecView: SpecView = SpecView(self)
        self._clean_spec = deepcopy(self.SpecView.generate_spec())
        self.PlusButton: QPushButton = QPushButton(ButtonActions.BUTTON_PLUS_SIGN)
        self.MinusButton: QPushButton = QPushButton(ButtonActions.BUTTON_MINUS_SIGN)
        self.NextLevelButton: QPushButton = QPushButton(ButtonActions.BUTTON_NEXT_LEVEL_SIGN)

        widgets_layouts_map = {
            self.PlusLayout: self.PlusButton,
            self.MinusLayout: self.MinusButton,
            self.NextLevelLayout: self.NextLevelButton,
            self.SpecTreeLayout: self.SpecView,
        }

        button_menu_structure = {
            self.ButtonApply: {
                ButtonActions.ONE_SESSION: lambda: self.apply(ButtonActions.ONE_SESSION),
                ButtonActions.PERMANENTLY: lambda: self.apply(ButtonActions.PERMANENTLY),
            },
            self.ButtonReset: {
                ButtonActions.LOCAL_SPEC: lambda: self.reset_spec.emit(ButtonActions.LOCAL_SPEC),
                ButtonActions.REMOTE_SPEC: lambda: self.reset_spec.emit(ButtonActions.REMOTE_SPEC),
            },
        }

        for button, button_actions in button_menu_structure.items():
            button.setMenu(QMenu())

            for name, action in button_actions.items():
                button.menu().addAction(name, action)
                button.menu().addSeparator()

            for action in button.menu().actions():
                if self.config.remote_spec.use_remote_spec:
                    break

                if action.text() == ButtonActions.REMOTE_SPEC:
                    action.setText(f"{action.text()} (disabled in configuration)")
                    action.setDisabled(True)
                    break

        for layout, widget in widgets_layouts_map.items():
            layout.addWidget(widget)

        for box in (self.CheckBoxHideReverved, self.CheckBoxReadOnly):
            box.setChecked(bool(Qt.CheckState.Checked))

        self.create_spec_logger()
        self.connect_all()
        self.set_read_only(self.CheckBoxReadOnly.isChecked())
        self.set_hello_message()

    def connect_all(self):

        connection_map = {
            self.SpecView.search_finished: self.hide_reserved_for_future,
            self.CheckBoxReadOnly.stateChanged: lambda state: self.set_read_only(bool(state)),
            self.CheckBoxHideReverved.stateChanged: self.hide_reserved_for_future,
            self.ParseFile.pressed: self.parse_file,
            self.spec_accepted: lambda name: info(f"Specification applied - {name}"),
            self.SearchLine.textChanged: self.SpecView.search,
            self.SearchLine.editingFinished: self.SpecView.setFocus,
            self.reset_spec: self.reload_spec,
            self.connector.got_remote_spec: self.process_remote_spec,
            self.load_remote_spec: self.connector.set_remote_spec,
        }

        buttons_connection_map = {
            self.ButtonClearLog: self.clear_log,
            self.ButtonCopyLog: self.copy_log,
            self.PlusButton: self.SpecView.plus,
            self.MinusButton: self.minus,
            self.NextLevelButton: self.SpecView.next_level,
            self.ButtonClose: self.close,
            self.ButtonReset: self.reload,
            self.ButtonClean: self.clean,
            self.ButtonSetMti: self.set_mti,
            self.ButtonBackup: self.backup,
            self.ButtonSetValidators: self.set_field_params,
        }

        keys_connection_map = {
            QKeySequence.StandardKey.Find: self.SearchLine.setFocus,
            QKeySequence.StandardKey.New: self.SpecView.plus,
            QKeySequence.StandardKey.Delete: self.SpecView.minus,
            QKeySequence.StandardKey.Open: self.parse_file,
            QKeySequence.StandardKey.Save: self.backup,
            KeySequence.CTRL_SHIFT_N: self.SpecView.next_level,
            KeySequence.CTRL_W: lambda: self.SpecView.edit_column(SpecFieldDef.ColumnsOrder.FIELD),
            KeySequence.CTRL_E: lambda: self.SpecView.edit_column(SpecFieldDef.ColumnsOrder.DESCRIPTION),
            KeySequence.CTRL_T: self.set_hello_message,
            KeySequence.CTRL_L: self.clear_log,
        }

        for signal, slot in connection_map.items():
            signal.connect(slot)

        for combination, function in keys_connection_map.items():  # Key sequences
            QShortcut(QKeySequence(combination), self).activated.connect(function)

        for button, function in buttons_connection_map.items():
            button.clicked.connect(function)

    @staticmethod
    def backup():
        rotator: SpecFilesRotator = SpecFilesRotator()
        backup_filename = rotator.backup_spec()
        info(f"Backup done! Filename: {backup_filename}")

    def set_hello_message(self):
        self.LogArea.setText(f"{TextConstants.HELLO_MESSAGE}\n")

    def process_remote_spec(self):
        self.SpecView.parse_spec(self.spec.spec)

    def copy_log(self):
        self.set_clipboard_text(self.LogArea.toPlainText())

    def set_read_only(self, checked: bool):
        self.read_only = checked

        for button in (self.PlusButton, self.MinusButton, self.NextLevelButton):
            button.setDisabled(checked)

    def clean(self):
        self.SpecView.clean()

    def clear_log(self):
        self.LogArea.setText(str())

    def hide_reserved_for_future(self):
        if self.SearchLine.text():
            return

        self.SpecView.hide_reserved(bool(self.CheckBoxHideReverved.checkState().value))

    def minus(self):
        self.SpecView.minus()

    def create_spec_logger(self):
        formatter = Formatter(LogDefinition.FORMAT, LogDefinition.DISPLAY_DATE_FORMAT, LogDefinition.MARK_STYLE)
        self.wireless_handler = WirelessHandler()
        stream = LogStream(self.LogArea)
        self.wireless_handler.new_record_appeared.connect(lambda record: stream.write(data=record))
        self.wireless_handler.setFormatter(formatter)
        getLogger().addHandler(self.wireless_handler)

    def reload_spec(self, spec_type: str):
        if spec_type == ButtonActions.LOCAL_SPEC:
            self.parse_file(TermFilesPath.SPECIFICATION)
            self.apply(commit=False)

        if spec_type == ButtonActions.REMOTE_SPEC:
            self.load_remote_spec.emit(False)

        self.reload()

    def set_mti_list(self, mti_list):
        self.spec.spec.mti = mti_list

    def set_mti(self):
        mti_window = MtiSpecWindow()
        mti_window.need_to_set_mti.connect(self.set_mti_list)
        mti_window.exec()

    def set_field_params(self):
        if not self.SpecView.hasFocus():
            self.SpecView.setFocus()

        item: SpecItem = self.SpecView.currentItem()

        if not item or item is self.SpecView.root:
            return

        if not (field_spec := item.get_field_spec()):
            error(f"Cannot get field specification for {item.get_field_path(string=True)}")
            return

        validator_window = FieldDataSet(field_spec)
        validator_window.field_spec_accepted.connect(self.process_field_spec_acceptance)
        validator_window.exec()

    def process_field_spec_acceptance(self, field_spec: IsoField):
        try:
            self.spec.set_field_spec(field_spec)
            self.SpecView.parse_field_spec(field_spec)

        except (ValidationError, ValueError) as validation_error:
            error(validation_error)

    @staticmethod
    def set_clipboard_text(data: str = str()) -> None:
        QApplication.clipboard().setText(data)

    def apply(self, commit: bool | str):
        if isinstance(commit, str):
            commit: bool = True if commit == ButtonActions.PERMANENTLY else False

        try:
            self.SpecView.reload_spec(commit)

        except Exception as apply_error:
            error(apply_error)
            self.spec_rejected.emit()
            return

        self._clean_spec = deepcopy(self.SpecView.generate_spec())
        self.spec_accepted.emit(self.spec.name)
        self.accepted.emit()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.process_close(a0)

    def parse_file(self, filename: Optional[str] = None) -> None:
        if filename is None:
            try:
                filename = QFileDialog.getOpenFileName()[0]
            except Exception as get_file_error:
                error(f"Filename get error: {get_file_error}")
                return

        if not filename:
            info("No input filename recognized")
            return

        try:
            with open(filename) as json_file:
                specification: EpaySpecModel = EpaySpecModel.model_validate_json(json_file.read())

        except ValidationError as validation_error:
            error_text = str(validation_error)
            error(f"File validation error: {error_text}")

        except Exception as parsing_error:
            error(f"File parsing error: {parsing_error}")

        else:
            self.SpecView.parse_spec(specification)

    def reload(self):
        self.SpecView.reload()
        self.CheckBoxHideReverved.setCheckState(Qt.CheckState.Checked)
        self.SpecView.hide_reserved()

    def process_close(self, close_event):
        try:
            current_spec = self.SpecView.generate_spec()

        except (ValidationError, ValueError) as spec_error:
            if isinstance(spec_error, ValidationError):
                error(spec_error)

            close_event.accept()
            return

        if current_spec == self._clean_spec:
            close_event.accept()
            return

        window = SpecUnsaved()
        window.return_to_spec.connect(close_event.ignore)
        window.return_to_spec.connect(window.accept)
        window.save.connect(self.apply)

        self.spec_rejected.connect(close_event.ignore)

        window.exec()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()
