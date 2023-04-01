from PyQt6.QtCore import Qt
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.gui.constants.SpecFieldDef import SpecFieldDef
from common.gui.core.AbstractItem import AbstractItem


class SpecItem(AbstractItem):
    _spec: IsoField = None
    _field_number: str = None
    _min_length: int
    _max_length: int
    _var_length: int
    _tag_length: int
    _description: str
    _reserved_for_future: bool
    _generate: bool
    _reversal: bool
    _matching: bool
    _alpha: bool
    _numeric: bool
    _special: bool
    _bytes: bool

    @property
    def tag_length(self):
        try:
            return int(self.text(SpecFieldDef.get_column_position(SpecFieldDef.TAG_LENGTH)))
        except ValueError:
            return int()

    @property
    def min_length(self):
        try:
            return int(self.text(SpecFieldDef.get_column_position(SpecFieldDef.MIX_LENGTH)))
        except ValueError:
            return int()

    @property
    def max_length(self):
        try:
            return int(self.text(SpecFieldDef.get_column_position(SpecFieldDef.MAX_LENGTH)))
        except ValueError:
            return int()

    @property
    def var_length(self):
        try:
            return int(self.text(SpecFieldDef.get_column_position(SpecFieldDef.VARIABLE_LENGTH)))
        except ValueError:
            return int()

    @property
    def description(self):
        return self.text(SpecFieldDef.get_column_position(SpecFieldDef.DESCRIPTION))

    @property
    def reserved_for_future(self):
        return self.text(SpecFieldDef.get_column_position(SpecFieldDef.DESCRIPTION)) == "Reserved for future"

    @property
    def generate(self):
        return bool(self.checkState(SpecFieldDef.get_column_position(SpecFieldDef.CAN_BE_GENERATED)))

    @property
    def reversal(self):
        return bool(self.checkState(SpecFieldDef.get_column_position(SpecFieldDef.USE_FOR_REVERSAL)))

    @property
    def matching(self):
        return bool(self.checkState(SpecFieldDef.get_column_position(SpecFieldDef.USE_FOR_MATCHING)))

    @property
    def alpha(self):
        return bool(self.checkState(SpecFieldDef.get_column_position(SpecFieldDef.ALPHA)))

    @property
    def numeric(self):
        return bool(self.checkState(SpecFieldDef.get_column_position(SpecFieldDef.NUMERIC)))

    @property
    def special(self):
        return bool(self.checkState(SpecFieldDef.get_column_position(SpecFieldDef.SPECIAL)))

    @property
    def bytes(self):
        return bool(self.checkState(SpecFieldDef.get_column_position(SpecFieldDef.BYTES)))

    # @property
    # def protected(self):
    #     return self._protected

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec: IsoField):
        self._spec: IsoField = spec

    @property
    def field_number(self):
        return self._field_number

    @field_number.setter
    def field_number(self, field_number: str):
        try:
            if not field_number.isdigit():
                return
        except AttributeError:
            return

        self._field_number = field_number

    def __init__(self, field_data: list[str], checkboxes: dict[str, bool] = None):
        super(SpecItem, self).__init__(field_data)

        try:
            self.field_number = field_data[0]
        except IndexError:
            self.field_number = None

        self.setup(checkboxes=checkboxes)

    def setup(self, checkboxes=None):
        if checkboxes is None:
            checkboxes = dict()

            for box in SpecFieldDef.get_checkbox_positions():
                checkboxes[box] = False

        self.set_checkboxes(checkboxes)
        self.field_number = self.text(SpecFieldDef.get_column_position(SpecFieldDef.FIELD))
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
