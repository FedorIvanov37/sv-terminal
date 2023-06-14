from PyQt6.QtCore import Qt
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.gui.constants.SpecFieldDef import SpecFieldDef
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
        return self.text(SpecFieldDef.get_column_position(SpecFieldDef.TAG_LENGTH))

    @property
    def min_length(self):
        return self.text(SpecFieldDef.get_column_position(SpecFieldDef.MIN_LENGTH))

    @property
    def max_length(self):
        return self.text(SpecFieldDef.get_column_position(SpecFieldDef.MAX_LENGTH))

    @property
    def var_length(self):
        return self.text(SpecFieldDef.get_column_position(SpecFieldDef.VARIABLE_LENGTH))

    @property
    def description(self):
        return self.text(SpecFieldDef.get_column_position(SpecFieldDef.DESCRIPTION))

    @property
    def reserved_for_future(self):
        return self.text(SpecFieldDef.get_column_position(SpecFieldDef.DESCRIPTION)) == "Reserved for future"

    @property
    def generate(self):
        return self.is_checked(SpecFieldDef.CAN_BE_GENERATED)

    @property
    def reversal(self):
        return self.is_checked(SpecFieldDef.USE_FOR_REVERSAL)

    @property
    def matching(self):
        return self.is_checked(SpecFieldDef.USE_FOR_MATCHING)

    @property
    def alpha(self):
        return self.is_checked(SpecFieldDef.ALPHA)

    @property
    def numeric(self):
        return self.is_checked(SpecFieldDef.NUMERIC)

    @property
    def special(self):
        return self.is_checked(SpecFieldDef.SPECIAL)

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec: IsoField):
        self._spec: IsoField = spec

    @property
    def field_number(self):
        return self.text(SpecFieldDef.get_column_position(SpecFieldDef.FIELD))

    def __init__(self, field_data: list[str], checkboxes: dict[str, bool] = None):
        super(SpecItem, self).__init__(field_data)
        self.setup(checkboxes=checkboxes)

    def setup(self, checkboxes=None):
        if checkboxes is None:
            checkboxes = dict()

            for box in SpecFieldDef.get_checkbox_positions():
                checkboxes[box] = False

        self.set_checkboxes(checkboxes)
        # self.field_number = self.text(SpecFieldDef.get_column_position(SpecFieldDef.FIELD))
        self.spec = self.epay_spec.get_field_spec(self.get_field_path())

    def set_checkboxes(self, checkboxes):
        if not checkboxes:
            return

        if self.text(SpecFieldDef.get_column_position(SpecFieldDef.FIELD)) == "Specification":
            return

        if self.field_number == self.epay_spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY:
            return

        [self.set_checkbox(int(column), state) for column, state in checkboxes.items()]

    def set_checkbox(self, column: int, checked: bool = True) -> None:
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        self.setCheckState(column, state)

    def is_checked(self, column):
        if not (column_position := SpecFieldDef.get_column_position(column)):
            return False

        state = self.checkState(column_position)
        state = state.value
        state = bool(state)

        return state
