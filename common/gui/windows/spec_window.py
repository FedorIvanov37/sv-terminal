from logging import error, info
from json import load
from typing import Optional
from pydantic import ValidationError
from PyQt6.QtGui import QCloseEvent, QKeyEvent, QKeySequence, QShortcut
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QMenu, QDialog, QPushButton, QApplication
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.EpaySpecificationModel import EpaySpecModel
from common.lib.constants import TermFilesPath
from common.gui.windows.spec_unsaved import SpecUnsaved
from common.gui.forms.spec import Ui_SpecificationWindow
from common.gui.core.json_views.SpecView import SpecView
from common.gui.windows.mti_spec_window import MtiSpecWindow
from common.gui.constants import ButtonActions, SpecFieldDef, KeySequence
from common.gui.decorators.window_settings import set_window_icon, has_close_button_only
from common.lib.constants import TextConstants
from common.gui.core.WirelessHandler import WirelessHandler
from common.lib.core.Logger import LogStream, getLogger, Formatter
from common.lib.constants import LogDefinition


class SpecWindow(Ui_SpecificationWindow, QDialog):
    _read_only: bool = True
    _spec: EpaySpecification = EpaySpecification()
    _spec_accepted: pyqtSignal = pyqtSignal(str)
    _spec_rejected: pyqtSignal = pyqtSignal()
    _reset_spec: pyqtSignal = pyqtSignal(str)

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

    def __init__(self, connector):
        super(SpecWindow, self).__init__()
        self.connector = connector
        self.setupUi(self)
        self._setup()

    @set_window_icon
    @has_close_button_only
    def _setup(self):
        self.PlusButton: QPushButton = QPushButton(ButtonActions.BUTTON_PLUS_SIGN)
        self.MinusButton: QPushButton = QPushButton(ButtonActions.BUTTON_MINUS_SIGN)
        self.NextLevelButton: QPushButton = QPushButton(ButtonActions.BUTTON_NEXT_LEVEL_SIGN)
        self.SpecView: SpecView = SpecView(self)
        #
        self.PlusLayout.addWidget(self.PlusButton)
        self.MinusLayout.addWidget(self.MinusButton)
        self.NextLevelLayout.addWidget(self.NextLevelButton)
        self.SpecTreeLayout.addWidget(self.SpecView)
        self.ButtonApply.setMenu(QMenu())
        self.ButtonReset.setMenu(QMenu())
        #
        self.ButtonApply.menu().addAction(ButtonActions.ONE_SESSION, lambda: self.apply(ButtonActions.ONE_SESSION))
        self.ButtonApply.menu().addSeparator()
        self.ButtonApply.menu().addAction(ButtonActions.PERMANENTLY, lambda: self.apply(ButtonActions.PERMANENTLY))
        self.ButtonReset.menu().addAction(ButtonActions.REMOTE_SPEC, lambda: self.reset_spec.emit(ButtonActions.REMOTE_SPEC))
        self.ButtonApply.menu().addSeparator()
        self.ButtonReset.menu().addAction(ButtonActions.LOCAL_SPEC, lambda: self.reset_spec.emit(ButtonActions.LOCAL_SPEC))

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

    def backup(self):
        backup_filename = self.spec.backup()
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
        wireless_handler = WirelessHandler()
        stream = LogStream(self.LogArea)
        wireless_handler.new_record_appeared.connect(lambda record: stream.write(data=record))
        wireless_handler.setFormatter(formatter)
        logger = getLogger()
        logger.addHandler(wireless_handler)

    def reload_spec(self, spec_type: str):
        if spec_type == ButtonActions.LOCAL_SPEC:
            self.parse_file(TermFilesPath.SPECIFICATION)

        if spec_type == ButtonActions.REMOTE_SPEC:
            self.connector.set_remote_spec(commit=False)

        self.reload()

    def set_mti_list(self, mti_list):
        self.spec.spec.mti = mti_list

    def set_mti(self):
        mti_window = MtiSpecWindow()
        mti_window.need_to_set_mti.connect(self.set_mti_list)
        mti_window.exec()

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
                specification: EpaySpecModel = EpaySpecModel.model_validate(load(json_file))

        except ValidationError as validation_error:
            error_text = str(validation_error)  # .json(indent=4)
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
        if self.SpecView.generate_spec() == self.spec.spec:
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
