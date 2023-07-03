from PyQt6.QtCore import Qt
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.gui.constants.SpecFieldDef import SpecFieldDefinition
from common.gui.core.AbstractItem import AbstractItem
from common.lib.core.EpaySpecification import EpaySpecification


class SpecItem(AbstractItem):
    _spec: IsoField = None
    _field_number: str = None
    _epay_spec: EpaySpecification = EpaySpecification()

    @property
    def epay_spec(self):
        return self._epay_spec

    @property
    def tag_length(self):
        return self.text(SpecFieldDefinition.ColumnsOrder.TAG_LENGTH)

    @property
    def min_length(self):
        return self.text(SpecFieldDefinition.ColumnsOrder.MIN_LENGTH)

    @property
    def max_length(self):
        return self.text(SpecFieldDefinition.ColumnsOrder.MAX_LENGTH)

    @property
    def var_length(self):
        return self.text(SpecFieldDefinition.ColumnsOrder.VARIABLE_LENGTH)

    @property
    def description(self):
        return self.text(SpecFieldDefinition.ColumnsOrder.DESCRIPTION)

    @property
    def reserved_for_future(self):
        return self.text(SpecFieldDefinition.ColumnsOrder.DESCRIPTION) == "Reserved for future"

    @property
    def generate(self):
        return self.is_checked(SpecFieldDefinition.ColumnsOrder.CAN_BE_GENERATED)

    @property
    def reversal(self):
        return self.is_checked(SpecFieldDefinition.ColumnsOrder.USE_FOR_REVERSAL)

    @property
    def matching(self):
        return self.is_checked(SpecFieldDefinition.ColumnsOrder.USE_FOR_MATCHING)

    @property
    def alpha(self):
        return self.is_checked(SpecFieldDefinition.ColumnsOrder.ALPHA)

    @property
    def numeric(self):
        return self.is_checked(SpecFieldDefinition.ColumnsOrder.NUMERIC)

    @property
    def special(self):
        return self.is_checked(SpecFieldDefinition.ColumnsOrder.SPECIAL)

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec: IsoField):
        self._spec: IsoField = spec

    @property
    def field_number(self):
        return self.text(SpecFieldDefinition.ColumnsOrder.FIELD)

    def __init__(self, field_data: list[str], checkboxes: dict[str, bool] = None):
        super(SpecItem, self).__init__(field_data)
        self.setup(checkboxes=checkboxes)

    def setup(self, checkboxes=None):
        if checkboxes is None:
            checkboxes = dict()

            for box in SpecFieldDefinition.CHECKBOXES:
                checkboxes[box] = False

        self.set_checkboxes(checkboxes)
        self.spec = self.epay_spec.get_field_spec(self.get_field_path())

    def set_checkboxes(self, checkboxes):
        if not checkboxes:
            return

        if self.text(SpecFieldDefinition.ColumnsOrder.FIELD) == "Specification":
            return

        if self.field_number == self.epay_spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY:
            return

        [self.set_checkbox(int(column), state) for column, state in checkboxes.items()]

    def set_checkbox(self, column: int, checked: bool = True) -> None:
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        self.setCheckState(column, state)

    def is_checked(self, column):
        state = self.checkState(column)
        state = state.value
        state = bool(state)

        return state
