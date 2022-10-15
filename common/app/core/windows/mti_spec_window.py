from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QCheckBox, QHBoxLayout, QWidget
from common.app.constants.FilePath import FilePath
from common.app.forms.mti_spec import Ui_MtiSpecWindow
from common.app.data_models.epay_specification import Mti
from common.app.core.tools.epay_specification import EpaySpecification


class MtiSpecWindow(Ui_MtiSpecWindow, QDialog):
    _spec: EpaySpecification = EpaySpecification()
    _changed: pyqtSignal = pyqtSignal()
    _need_to_set_mti: pyqtSignal = pyqtSignal(list)

    @property
    def need_to_set_mti(self):
        return self._need_to_set_mti

    @property
    def changed(self):
        return self._changed

    @property
    def spec(self):
        return self._spec

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(FilePath.MAIN_LOGO))
        self.ButtonPlus.clicked.connect(self.plus)
        self.ButtonMinus.clicked.connect(self.minus)
        self.ButtonSave.clicked.connect(self.ok)
        self.ButtonCancel.clicked.connect(self.cancel)
        self.parse_mti_list(self.spec.spec.mti)
        self.MtiTable.verticalHeader().hide()
        self.ButtonPlus.setDisabled(True)
        self.ButtonMinus.setDisabled(True)
        self.MtiTable.itemChanged.connect(self.changed.emit)

    def plus(self):
        ...

    def minus(self):
        ...

    def ok(self):
        mti_list = self.create_mti_list()
        self.need_to_set_mti.emit(mti_list)
        self.accept()

    def cancel(self):
        self.close()

    def parse_mti_list(self, mti_list: list[Mti]):
        for row_count, mti in enumerate(mti_list):
            row_set = (mti.description, mti.request, mti.response, mti.is_reversible, mti.reversal_mti)
            self.MtiTable.insertRow(row_count)

            for item_count, item_data in enumerate(row_set):
                item = self.MtiItem(self.MtiTable, item_data)

                if isinstance(item_data, bool):
                    item.set_checkbox(item_data, row_count, item_count)

                self.MtiTable.setItem(row_count, item_count, item)

        self.MtiTable.horizontalHeader().setSectionResizeMode(self.MtiTable.horizontalHeader().ResizeToContents)

    def create_mti_list(self) -> list[Mti] | None:
        result: list = list()

        for row in range(self.MtiTable.rowCount()):
            mti_list = list()

            for column in range(self.MtiTable.columnCount()):
                if not (item := self.MtiTable.item(row, column)):
                    continue

                item_data: bool | str = item.checked if item.checkbox else item.text()

                mti_list.append(item_data)

            mti: Mti = Mti()
            mti.description, mti.request, mti.response, mti.is_reversible, mti.reversal_mti = mti_list
            result.append(mti)

        return result

    class MtiItem(QTableWidgetItem):
        _changed: bool = False
        _checked: bool = False
        _checkbox: QCheckBox = None

        @property
        def changed(self):
            return self._changed

        @changed.setter
        def changed(self, changed):
            self._changed = changed

        @property
        def checkbox(self):
            return self._checkbox

        @checkbox.setter
        def checkbox(self, checkbox):
            self._checkbox = checkbox

        @property
        def checked(self):
            if not self.checkbox:
                return False

            return self.checkbox.isChecked()

        def __init__(self, mti_table, item_data):
            super().__init__(item_data)
            self.MtiTable = mti_table

        def set_checkbox(self, state: bool, row_number: int, column_number: int) -> None:
            self.changed = True
            cell_widget = QWidget()
            self.checkbox: QCheckBox = QCheckBox()
            self.checkbox.setChecked(state)
            self.checkbox.setText(" ")
            lay_out = QHBoxLayout(cell_widget)
            lay_out.addWidget(self.checkbox)
            lay_out.setAlignment(Qt.AlignCenter)
            lay_out.setContentsMargins(0, 0, 0, 0)
            cell_widget.setLayout(lay_out)
            self.MtiTable.setCellWidget(row_number, column_number, cell_widget)
