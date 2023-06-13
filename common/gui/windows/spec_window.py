from json import dumps
from typing import Optional
from datetime import datetime
from pydantic import ValidationError
from PyQt6.QtGui import QIcon, QCloseEvent, QKeyEvent
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QMenu, QDialog, QPushButton
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.EpaySpecificationModel import EpaySpecModel
from common.gui.windows.spec_unsaved import SpecUnsaved
from common.gui.forms.spec import Ui_SpecificationWindow
from common.gui.constants.TermFilesPath import TermFilesPath
from common.gui.core.SpecView import SpecView
from common.gui.windows.mti_spec_window import MtiSpecWindow


class SpecWindow(Ui_SpecificationWindow, QDialog):
    _changed: bool = False
    _mti_changed: bool = False
    _read_only: bool = True
    _spec: EpaySpecification = EpaySpecification()
    _spec_accepted: pyqtSignal = pyqtSignal(str)
    _need_to_close: bool = False

    @property
    def need_to_close(self):
        return self._need_to_close

    @need_to_close.setter
    def need_to_close(self, need_to_close):
        self._need_to_close = need_to_close

    @property
    def spec_accepted(self):
        return self._spec_accepted

    @property
    def changed(self):
        return self._changed

    @changed.setter
    def changed(self, changed):
        self._changed = changed

    @property
    def spec(self):
        return self._spec

    @property
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, checked):
        self._read_only = checked

    def __init__(self, window):
        super(SpecWindow, self).__init__()
        self.setupUi(self)
        self.main_window = window
        self.setup()

    def setup(self):
        self.setWindowIcon(QIcon(TermFilesPath.MAIN_LOGO))
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        self.PlusButton = QPushButton("+")
        self.MinusButton = QPushButton("-")
        self.NextLevelButton = QPushButton("↵")
        self.PlusLayout.addWidget(self.PlusButton)
        self.MinusLayout.addWidget(self.MinusButton)
        self.NextLevelLayout.addWidget(self.NextLevelButton)
        self.SpecView: SpecView = SpecView(self.SpecTree, self)
        self.StatusLabel.setText(str())
        self.SpecTree.itemChanged.connect(self.item_changed)
        self.PlusButton.clicked.connect(self.SpecView.plus)
        self.MinusButton.clicked.connect(self.minus)
        self.NextLevelButton.clicked.connect(self.SpecView.next_level)
        self.ButtonClose.clicked.connect(self.close)
        self.ButtonReset.clicked.connect(self.reload)
        self.ButtonClean.clicked.connect(self.clean)
        self.SpecView.status_changed.connect(lambda status, error: self.set_status(status, error))
        self.CheckBoxReadOnly.stateChanged.connect(lambda state: self.set_read_only(bool(state)))
        self.CheckBoxHideReverved.stateChanged.connect(lambda state: self.SpecView.hide_reserved(bool(state)))
        self.ButtonBackup.clicked.connect(self.backup)
        self.ParseFile.pressed.connect(self.parse_file)
        self.ButtonSetMti.clicked.connect(self.set_mti)
        self.spec_accepted.connect(lambda name: self.set_status(f"Specification applied - {name}"))

        apply_menu = QMenu()

        for action in ("For current session", "Permanently"):  # TODO Hardcode
            apply_menu.addAction(action, self.apply)

        self.ButtonApply.setMenu(apply_menu)

        for box in (self.CheckBoxHideReverved, self.CheckBoxReadOnly):
            box.setChecked(bool(Qt.CheckState.Checked))

        self.set_status(">")

    def minus(self):
        self.changed = True
        self.SpecView.minus()

    def set_mti_list(self, mti_list):
        self.spec.spec.mti = mti_list
        self.changed = True

    def set_mti(self):
        mti_window = MtiSpecWindow()
        mti_window.need_to_set_mti.connect(self.set_mti_list)
        mti_window.changed.connect(self.set_mti_changed)
        mti_window.rejected.connect(lambda: self.set_mti_changed(changed=False))
        mti_window.exec()

    def set_mti_changed(self, changed=True):
        self._mti_changed = changed

    def set_read_only(self, checked: bool):
        self.read_only = checked

        for button in (self.PlusButton, self.MinusButton, self.NextLevelButton):
            button.setDisabled(checked)

    def clean(self):
        self.StatusLabel.setText(str())
        self.SpecView.clean()
    
    def apply(self, commit: bool = None):
        if commit is None:
            commit = self.sender().text().upper() == "PERMANENTLY"  # TODO Hardcode

        try:
            self.SpecView.reload_spec(commit)
        except Exception as E:
            self.set_status(str(E))
            return

        self.spec_accepted.emit(self.spec.name)
        self.changed = False

    def closeEvent(self, a0: QCloseEvent) -> None:
        if self.process_close():
            a0.accept()
            return

        a0.ignore()

    def item_changed(self, item, column):
        self.changed = True

    def backup(self):
        spec = self.SpecView.generate_spec()
        date_format = "%Y%m%d_%H%M%S"
        filename = f"spec_backup_{datetime.now():{date_format}}.json"

        with open(f'{TermFilesPath.SPEC_BACKUP_DIR}/{filename}', "w") as file:
            file.write(dumps(spec.dict(), indent=4))

        self.set_status("Backup done! Filename: %s" % filename)

    def parse_file(self, filename: Optional[str] = None) -> None:
        if filename is None:
            try:
                filename = QFileDialog.getOpenFileName()[0]
            except Exception as get_file_error:
                self.set_status("Filename get error: %s" % get_file_error, error=True)
                return

        if not filename:
            self.set_status("No input filename recognized")
            return

        try:
            specification: EpaySpecModel = EpaySpecModel.parse_file(filename)

        except ValidationError as validation_error:
            error_text = str(validation_error.json(indent=4))
            self.set_status("File validation error: %s" % error_text, error=True)

        except Exception as parsing_error:
            self.set_status("File parsing error: %s" % parsing_error)

        else:
            self.SpecView.parse_spec(specification)
            self.changed = True

    def reload(self):
        self.SpecView.reload()
        self.set_status(str())
        self.CheckBoxHideReverved.setCheckState(Qt.CheckState.Checked)
        self.SpecView.hide_reserved()

    def process_close(self) -> bool:
        self.need_to_close = True

        if self.changed or self._mti_changed:
            window = SpecUnsaved()
            window.save.connect(self.apply)
            window.return_to_spec.connect(self.set_need_to_close)
            window.exec()

        return self.need_to_close

    def set_need_to_close(self, need=False):
        self.need_to_close = need

    def set_status(self, text: str, error: bool = False) -> None:
        text_message = list()

        for position in range(0, len(text), 150):
            text_message.append(f"{text[position: position + 150]}")

        if error:
            self.StatusLabel.setStyleSheet("color: red")  # TODO Hardcode
            text_message[int()] = f"Error: {text_message[int()]}"
        else:
            self.StatusLabel.setStyleSheet("color: black")

        self.StatusLabel.setText("\n".join(text_message))

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()
