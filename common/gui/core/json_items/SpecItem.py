from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QWidget
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.gui.core.json_items.Item import Item
from common.gui.enums import SpecFieldDef
from common.gui.enums.RootItemNames import RootItemNames


class SpecItem(Item):
    _spec: IsoField = None
    _field_number: str = None

    @property
    def tag_length(self):
        return self.text(SpecFieldDef.ColumnsOrder.TAG_LENGTH)

    @property
    def min_length(self):
        return self.text(SpecFieldDef.ColumnsOrder.MIN_LENGTH)

    @property
    def max_length(self):
        return self.text(SpecFieldDef.ColumnsOrder.MAX_LENGTH)

    @property
    def var_length(self):
        return self.text(SpecFieldDef.ColumnsOrder.VARIABLE_LENGTH)

    @var_length.setter
    def var_length(self, var_length):
        self.setText(SpecFieldDef.ColumnsOrder.VARIABLE_LENGTH, var_length)

    @property
    def description(self):
        return self.text(SpecFieldDef.ColumnsOrder.DESCRIPTION)

    @property
    def reserved_for_future(self):
        try:
            return self.spec.reserved_for_future
        except AttributeError:
            self.set_spec()

        if not self.spec:
            return False

        return self.spec.reserved_for_future

    @property
    def generate(self):
        return self.is_checked(SpecFieldDef.ColumnsOrder.CAN_BE_GENERATED)

    @property
    def reversal(self):
        return self.is_checked(SpecFieldDef.ColumnsOrder.USE_FOR_REVERSAL)

    @property
    def matching(self):
        return self.is_checked(SpecFieldDef.ColumnsOrder.USE_FOR_MATCHING)

    @property
    def alpha(self):
        return self.is_checked(SpecFieldDef.ColumnsOrder.ALPHA)

    @property
    def numeric(self):
        return self.is_checked(SpecFieldDef.ColumnsOrder.NUMERIC)

    @property
    def special(self):
        return self.is_checked(SpecFieldDef.ColumnsOrder.SPECIAL)

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec: IsoField):
        self._spec: IsoField = spec

    @property
    def field_number(self):
        return self.text(SpecFieldDef.ColumnsOrder.FIELD)

    @property
    def is_secret(self):
        return self.is_checked(SpecFieldDef.ColumnsOrder.SECRET)

    def __init__(self, field_data: list[str] | None = None):
        if field_data is None:
            field_data: list[str] = list()

        super(SpecItem, self).__init__(field_data)

    def set_checkboxes(self, checkboxes: dict[int, bool]):
        if self.text(SpecFieldDef.ColumnsOrder.FIELD) == RootItemNames.SPECIFICATION_ROOT_NAME:
            return

        if self.field_number == self.epay_spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY:
            return

        if checkboxes is None:
            checkboxes: dict[int, bool] = dict()

            for box in SpecFieldDef.Checkboxes:
                checkboxes[box] = False

        for column, state in checkboxes.items():
            self.set_checkbox(column, Qt.CheckState.Checked if state else Qt.CheckState.Unchecked)

    def is_secret_pan(self, column: int) -> bool:
        secret_pan_conditions = (
            self.field_number == self.epay_spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER,
            column == SpecFieldDef.ColumnsOrder.SECRET,
        )

        return all(secret_pan_conditions)

    def set_checkbox(self, column: int, state: Qt.CheckState):
        checkbox = QCheckBox()
        checkbox.setCheckState(state)

        if self.is_secret_pan(column):
            checkbox.setCheckState(Qt.CheckState.PartiallyChecked)
            self.set_widget_read_only(checkbox)

        if column == SpecFieldDef.ColumnsOrder.CAN_BE_GENERATED and state == Qt.CheckState.Checked:
            checkbox.setCheckState(Qt.CheckState.PartiallyChecked)
            self.set_widget_read_only(checkbox)

        field_path = self.get_field_path()
        trans_id_path = self.epay_spec.get_trans_id_path()

        if field_path == trans_id_path and column == SpecFieldDef.ColumnsOrder.CAN_BE_GENERATED:
            checkbox.setCheckState(Qt.CheckState.PartiallyChecked)
            self.set_widget_read_only(checkbox)

        if not (tree := self.treeWidget()):
            return

        checkbox.stateChanged.connect(lambda: tree.itemChanged.emit(self, column))
        tree.removeItemWidget(self, column)
        tree.setItemWidget(self, column, checkbox)

    @staticmethod
    def set_widget_read_only(widget: QWidget, readonly: bool = True) -> None:
        if widget is None:
            return

        widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, readonly)
        widget.setFocusPolicy(Qt.FocusPolicy.NoFocus if readonly else Qt.FocusPolicy.StrongFocus)

    def set_readonly(self, readonly: bool = True):
        if not (tree := self.treeWidget()):
            return

        for column in SpecFieldDef.ColumnsOrder:
            if not (widget := tree.itemWidget(self, column)):
                continue

            read_only = readonly

            if self.is_secret_pan(column):
                read_only = True

            if column == SpecFieldDef.ColumnsOrder.CAN_BE_GENERATED:
                read_only = True

            self.set_widget_read_only(widget, read_only)

    def is_checked(self, column) -> bool:
        if not (tree := self.treeWidget()):
            return False

        if not (checkbox := tree.itemWidget(self, column)):
            return False

        if not isinstance(checkbox, QCheckBox):
            return False

        state = checkbox.isChecked()

        return state

    def parse_field_spec(self, field_spec: IsoField):
        column_values_map = {
            SpecFieldDef.ColumnsOrder.FIELD: field_spec.field_number,
            SpecFieldDef.ColumnsOrder.DESCRIPTION: field_spec.description,
            SpecFieldDef.ColumnsOrder.MIN_LENGTH: field_spec.min_length,
            SpecFieldDef.ColumnsOrder.MAX_LENGTH: field_spec.max_length,
            SpecFieldDef.ColumnsOrder.VARIABLE_LENGTH: field_spec.var_length,
            SpecFieldDef.ColumnsOrder.TAG_LENGTH: field_spec.tag_length,
        }

        column_checkboxes_map = {
            SpecFieldDef.ColumnsOrder.ALPHA: field_spec.alpha,
            SpecFieldDef.ColumnsOrder.NUMERIC: field_spec.numeric,
            SpecFieldDef.ColumnsOrder.SPECIAL: field_spec.special,
            SpecFieldDef.ColumnsOrder.USE_FOR_MATCHING: field_spec.matching,
            SpecFieldDef.ColumnsOrder.USE_FOR_REVERSAL: field_spec.reversal,
            SpecFieldDef.ColumnsOrder.CAN_BE_GENERATED: field_spec.generate,
        }

        if self.get_field_path(string=True) != self.epay_spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
            column_checkboxes_map[SpecFieldDef.ColumnsOrder.SECRET] = field_spec.is_secret

        for column, value in column_values_map.items():
            self.setText(column, str(value))

        self.set_checkboxes(column_checkboxes_map)
