from PyQt6.QtCore import Qt
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.gui.constants import SpecFieldDef
from common.gui.core.json_items.Item import Item


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

    def __init__(self, field_data: list[str], checkboxes: dict[int, bool] = None):
        super(SpecItem, self).__init__(field_data)
        self.setup(checkboxes=checkboxes)

    def setup(self, checkboxes=None):
        self.set_checkboxes(checkboxes)
        # self.setTextAlignment(SpecFieldDef.ColumnsOrder.ALPHA, Qt.AlignmentFlag.AlignCenter)

    def set_checkboxes(self, checkboxes: dict[str, bool]):
        if self.text(SpecFieldDef.ColumnsOrder.FIELD) == SpecFieldDef.SPECIFICATION:
            return

        if self.field_number == self.epay_spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY:
            return

        if checkboxes is None:
            checkboxes: dict[str, bool] = dict()

            for box in SpecFieldDef.CHECKBOXES:
                checkboxes[box] = False

        for column, state in checkboxes.items():
            self.setCheckState(int(column), Qt.CheckState.Checked if state else Qt.CheckState.Unchecked)

    def is_checked(self, column):
        state = self.checkState(column)
        state = state.value
        state = bool(state)
        return state
