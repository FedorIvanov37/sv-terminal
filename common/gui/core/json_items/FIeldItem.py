from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidgetItem, QCheckBox, QWidget
from common.lib.data_models.EpaySpecificationModel import IsoField
from common.lib.toolkit.toolkit import mask_pan, mask_secret
from common.lib.core.EpaySpecification import EpaySpecification
from common.gui.constants.MainFieldSpec import MainFieldSpec as FieldsSpec
from common.gui.core.json_items.Item import Item
from common.gui.constants.CheckBoxesDefinition import CheckBoxesDefinition
from common.gui.decorators.void_qt_signals import void_tree_signals


class FieldItem(Item):
    epay_spec: EpaySpecification = EpaySpecification()
    spec: IsoField = None
    _secret: str = ""
    _masked: bool = False

    @property
    def masked(self):
        return self._masked

    @masked.setter
    def masked(self, masked):
        self._masked = masked

    @property
    def field_data(self):
        if self.is_secret and self._secret:
            return self._secret

        return self.text(FieldsSpec.ColumnsOrder.VALUE)

    @field_data.setter
    def field_data(self, field_data):
        self.setText(FieldsSpec.ColumnsOrder.VALUE, field_data)
        self._secret = ""
        self.set_spec()
        self.hide_secret()

    @property
    def field_length(self):
        return self.text(FieldsSpec.ColumnsOrder.LENGTH)

    @property
    def field_number(self):
        return self.text(FieldsSpec.ColumnsOrder.FIELD)

    @property
    def is_secret(self):
        if not (spec := self.epay_spec.get_field_spec(self.get_field_path())):
            if not (spec := self.spec):
                return False

        return spec and spec.is_secret

    @property
    def description(self):
        return self.text(FieldsSpec.ColumnsOrder.DESCRIPTION)

    def __init__(self, item_data: list[str], spec=None):
        super(FieldItem, self).__init__(item_data)
        self.spec = spec if spec else self.spec
        self.setTextAlignment(FieldsSpec.ColumnsOrder.LENGTH, Qt.AlignmentFlag.AlignRight)

    def addChild(self, item, fill_len=None):
        item.spec = self.epay_spec.get_field_spec(item.get_field_path())
        QTreeWidgetItem.addChild(self, item)
        item.set_length(fill_length=fill_len)

    def hide_secret(self, hide_the_secret: bool | None = None):
        tree = self.treeWidget()

        if tree and not tree.hide_secret_fields:
            if self.field_number != self.epay_spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
                hide_the_secret = False
        
        if hide_the_secret is None:
            hide_the_secret: bool = self.is_secret

        if hide_the_secret:
            self.mask_secret_value()

        else:
            self.show_secret_value()

    @void_tree_signals
    def mask_secret_value(self):
        secret = self.field_data

        if self.field_number == self.epay_spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
            mask = mask_pan(secret)
        else:
            mask = mask_secret(secret)

        self.setText(FieldsSpec.ColumnsOrder.VALUE, mask)
        self._secret = secret
        self.masked = True

    @void_tree_signals
    def show_secret_value(self):
        if not self.masked:
            return

        self.setText(FieldsSpec.ColumnsOrder.VALUE, self._secret)
        self._secret = ""
        self.masked = False

    def checkbox_checked(self, checkbox_type: str):
        if checkbox_type not in (CheckBoxesDefinition.GENERATE, CheckBoxesDefinition.JSON_MODE):
            return False

        if checkbox_type == CheckBoxesDefinition.JSON_MODE:
            if not self.epay_spec.is_field_complex(self.get_field_path()):
                return False

        if checkbox_type == CheckBoxesDefinition.GENERATE:
            if self.field_number not in FieldsSpec.generated_fields:
                return False

        if not (tree := self.treeWidget()):
            return False

        checkbox: QWidget | QCheckBox = tree.itemWidget(self, FieldsSpec.ColumnsOrder.PROPERTY)

        if not isinstance(checkbox, QCheckBox):
            return False

        return bool(checkbox.checkState().value)

    @void_tree_signals
    def set_checkbox(self, checked=True):
        if self.get_field_depth() != 1:
            return

        column_number = FieldsSpec.ColumnsOrder.PROPERTY
        state = CheckBoxesDefinition.CHECKED if checked else CheckBoxesDefinition.UNCHECKED
        checkbox = QCheckBox()
        checkbox.setCheckState(state)

        if not (tree := self.treeWidget()):
            return

        tree.removeItemWidget(self, FieldsSpec.ColumnsOrder.PROPERTY)

        if self.field_number in FieldsSpec.generated_fields:
            checkbox.setText(CheckBoxesDefinition.GENERATE)
            tree.setItemWidget(self, column_number, checkbox)

        if self.epay_spec.is_field_complex(self.get_field_path()):
            checkbox.setText(CheckBoxesDefinition.JSON_MODE)
            tree.setItemWidget(self, column_number, checkbox)

        checkbox.stateChanged.connect(lambda: tree.itemChanged.emit(self, FieldsSpec.ColumnsOrder.PROPERTY))

    def process_change_item(self):
        self.set_spec()
        self.set_item_color()
        self.set_description()
        self.set_length()

    @void_tree_signals
    def set_description(self, text: str | None = None):
        if text is not None:
            self.setText(FieldsSpec.ColumnsOrder.DESCRIPTION, str(text))
            return

        if not self.spec:
            self.set_spec()

        self.setText(FieldsSpec.ColumnsOrder.DESCRIPTION, self.spec.description if self.spec else str())

    @void_tree_signals
    def set_length(self, length: int | None = None, fill_length: int | None = None) -> None:
        column = FieldsSpec.ColumnsOrder.LENGTH

        if not self.spec:
            self.set_spec()

        if length is None:
            length: int = self.get_field_length()

        if fill_length is None:
            try:
                fill_length = self.spec.var_length
            except AttributeError:
                fill_length = int()

        if not self.spec and self.field_length:
            fill_length = len(self.text(FieldsSpec.ColumnsOrder.LENGTH))

        length: str = str(length).zfill(fill_length)

        self.setText(column, str(length))

        if parent := self.parent():
            parent.set_length()

    def get_field_length(self):
        if self.childCount():
            length = sum([item.get_field_length() for item in self.get_children()])

        else:
            length = len(self.field_data)

        return length
