from typing import Callable
from logging import info, error, warning
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QTreeWidgetItem, QItemDelegate, QCheckBox
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.EpaySpecificationModel import EpaySpecModel, Validators
from common.lib.data_models.EpaySpecificationModel import IsoField, FieldSet
from common.lib.data_models.Types import FieldPath
from common.gui.core.json_items.SpecItem import SpecItem
from common.gui.core.validators.SpecValidator import SpecValidator
from common.gui.decorators.void_qt_signals import void_qt_signals
from common.gui.core.json_views.TreeView import TreeView
from common.gui.enums.Colors import Colors
from common.gui.enums import SpecFieldDef
from common.gui.enums.RootItemNames import RootItemNames


class SpecView(TreeView):
    _spec: EpaySpecification = EpaySpecification()
    search_finished = pyqtSignal()

    # Reject function execution when read only mode is active
    def reject_in_read_only_mode(fuction: Callable, *args, **kwargs):
        def wrapper(self, *args, **kwargs):
            if not self.window.read_only:
                return fuction(self)

            if not self.hasFocus():
                self.setFocus()

            warning("Read only mode. Uncheck the checkbox on top of the window")

        return wrapper

    @property
    def spec(self):
        return self._spec

    def __init__(self, window):
        super(SpecView, self).__init__()
        self.root: SpecItem = SpecItem([RootItemNames.SPECIFICATION_ROOT_NAME])
        self.window = window
        self.validator = SpecValidator()
        self.setItemDelegate(QItemDelegate())
        self._setup()

    def _setup(self):
        self.setHeaderLabels(SpecFieldDef.Columns)
        self.addTopLevelItem(self.root)
        self.itemDoubleClicked.connect(self.editItem)
        self.itemClicked.connect(self.process_item_click)
        self.itemChanged.connect(self.process_item_change)
        self.currentItemChanged.connect(self.print_path)
        self.parse_spec()
        self.make_order()
        self.collapseAll()
        self.root.setExpanded(True)
        self.resizeColumnToContents(SpecFieldDef.ColumnsOrder.DESCRIPTION)

    def print_path(self):
        item: SpecItem
        path: FieldPath

        if not (item := self.currentItem()):
            return

        if not (path := item.get_field_path()):
            return

        if not any((item.field_number, item.description)):
            return

        description: str = self.spec.get_field_description(path, string=True)
        path: str = item.get_field_path(string=True)

        info(f"{path} - {description}")

    def set_read_only(self, readonly: bool = True, parent: SpecItem | None = None) -> None:
        if parent is None:
            parent = self.root

        spec_item: SpecItem

        for spec_item in parent.get_children():
            spec_item.set_readonly(readonly)

            if not spec_item.get_children():
                continue

            self.set_read_only(readonly=readonly, parent=spec_item)

    @void_qt_signals
    def process_item_click(self, item: SpecItem, column: int) -> None:
        self.validate_item(item, column, validate_all=True)

        if item.is_secret_pan(column):
            warning("The Card Number is a secret constantly")
            return

        if column == SpecFieldDef.ColumnsOrder.CAN_BE_GENERATED:
            warning('Checkbox "Generate" is pre-defined, not possible to change the state')
            return

    @void_qt_signals
    def process_item_change(self, item: SpecItem, column: int):
        self.validate_item(item, column, validate_all=True)

        if column == SpecFieldDef.ColumnsOrder.SECRET:
            self.cascade_checkboxes(item)

        if column == SpecFieldDef.ColumnsOrder.TAG_LENGTH:
            self.cascade_tag_length(item)

    def search(self, text: str, parent: SpecItem | None = None) -> None:
        TreeView.search(self, text, parent)
        self.search_finished.emit()

    @staticmethod
    def cascade_tag_length(parent: SpecItem):
        child_item: SpecItem

        for child_item in parent.get_children():
            child_item.var_length = parent.tag_length

    @void_qt_signals
    def cascade_checkboxes(self, parent: SpecItem):
        check_state = parent.checkState(SpecFieldDef.ColumnsOrder.SECRET)

        for item in parent.get_children():
            item.setCheckState(SpecFieldDef.ColumnsOrder.SECRET, check_state)

            if item.childCount():
                self.cascade_checkboxes(item)

    def editItem(self, item, column):
        if item is self.root and column not in (SpecFieldDef.ColumnsOrder.DESCRIPTION, SpecFieldDef.ColumnsOrder.FIELD):
            return

        if column > SpecFieldDef.ColumnsOrder.TAG_LENGTH:
            return

        if column == SpecFieldDef.ColumnsOrder.CAN_BE_GENERATED:
            return

        if self.window.read_only:
            warning("Read only mode. Uncheck the checkbox on top of the window")
            return

        TreeView.editItem(self, item, column)

    def validate_item(self, item: SpecItem, column: int, validate_all=False):
        if item is self.root:
            return

        try:
            if validate_all:
                self.validator.validate_spec_row(item)

            else:
                self.validator.validate_column(item, column)

        except ValueError as validation_error:
            error(validation_error)
            item.set_item_color(Colors.RED)
            return

        item.set_item_color()

    def hide_reserved(self, hide=True):
        item: SpecItem

        for item in self.root.get_children():

            if item.reserved_for_future:
                item.setHidden(hide)

    def reload_spec(self, commit):
        spec: EpaySpecModel = self.generate_spec()
        self.spec.reload_spec(spec, commit)

    def reload(self):
        self.setup()

    def make_order(self):
        TreeView.make_order(self)
        self.hide_reserved()

    @reject_in_read_only_mode
    def minus(self):
        item: SpecItem = self.currentItem()

        if item is None:
            return

        if item is self.root:
            self.setCurrentItem(self.root)
            self.setFocus()
            return

        self.setFocus()

        parent: SpecItem = item.parent()

        parent.takeChild(parent.indexOfChild(item))

    @reject_in_read_only_mode
    def plus(self):
        item = SpecItem([])

        if not (current_item := self.currentItem()):
            return

        parent = current_item.parent()

        if parent is None:
            return

        current_index = parent.indexOfChild(current_item)
        parent.insertChild(current_index + 1, item)
        self.scrollToItem(item)
        self.editItem(item, 0)
        self.setCurrentItem(item)

    @reject_in_read_only_mode
    def next_level(self):
        item = SpecItem([])
        current_item: SpecItem = self.currentItem()

        if current_item is None:
            return

        self.currentItem().addChild(item)
        self.setCurrentItem(item)
        self.editItem(item, int())

    @void_qt_signals
    def parse_field_spec(self, field_spec: IsoField):
        if not(item := self.get_item_by_path(field_spec.field_path)):
            return

        item.parse_field_spec(field_spec)

    def parse_spec(self, spec=None):
        if spec is None:
            spec = self.spec

        current_path = None
        current_item: SpecItem

        if current_item := self.currentItem():
            current_path = current_item.get_field_path()

        self.clean()
        self.root.setText(SpecFieldDef.ColumnsOrder.DESCRIPTION, spec.name)
        self.parse_spec_fields(spec.fields)
        self.collapseAll()
        self.expandItem(self.root)
        self.set_current_item_by_path(current_path)

    def get_item_by_path(self, field_path: FieldPath, parent: SpecItem | None = None) -> SpecItem:
        if parent is None:
            parent = self.root

        for child in parent.get_children():
            if child.get_field_path() == field_path:
                return child

            if child.get_children():
                if child := self.get_item_by_path(field_path, parent=child):
                    return child

    def set_current_item_by_path(self, field_path: FieldPath, parent: SpecItem | None = None):
        if parent is None:
            parent = self.root

        for item in parent.get_children():
            if item.get_field_path() == field_path:
                self.setCurrentItem(item)
                self.scrollToItem(item)
                return

            if item.get_children():
                self.set_current_item_by_path(field_path=field_path, parent=item)

    def parse_spec_fields(self, input_json, parent: QTreeWidgetItem = None):
        if parent is None or parent == self.root:
            parent = self.root

        for field in sorted(input_json, key=int):

            if field == self.spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY:
                continue

            field_data: IsoField = input_json[field]

            field_data_for_item = [
                field,
                field_data.description,
                field_data.min_length,
                field_data.max_length,
                field_data.var_length,
                field_data.tag_length,
            ]

            field_data_for_item: list[str] = list(map(str, field_data_for_item))

            checkboxes: dict[int, bool] = {
                SpecFieldDef.ColumnsOrder.USE_FOR_MATCHING: field_data.matching,
                SpecFieldDef.ColumnsOrder.USE_FOR_REVERSAL: field_data.reversal,
                SpecFieldDef.ColumnsOrder.CAN_BE_GENERATED: field_data.generate,
                SpecFieldDef.ColumnsOrder.ALPHA: field_data.alpha,
                SpecFieldDef.ColumnsOrder.NUMERIC: field_data.numeric,
                SpecFieldDef.ColumnsOrder.SPECIAL: field_data.special,
                SpecFieldDef.ColumnsOrder.SECRET: field_data.is_secret
            }

            item: SpecItem = SpecItem(field_data_for_item)

            parent.addChild(item)

            item.set_checkboxes(checkboxes)

            if field_data.fields:
                self.parse_spec_fields(input_json=field_data.fields, parent=item)

        self.make_order()

    def generate_spec(self) -> EpaySpecModel:
        name: str = self.root.text(SpecFieldDef.ColumnsOrder.DESCRIPTION)
        fields_set: FieldSet

        def generate_fields(spec_item: SpecItem = None) -> FieldSet:
            if spec_item is None:
                spec_item = self.root

            fields: FieldSet = dict()

            row: SpecItem

            for row in spec_item.get_children():
                self.validator.validate_spec_row(row)

                field = IsoField(
                    field_number=row.field_number,
                    field_path=row.get_field_path(),
                    min_length=row.min_length,
                    max_length=row.max_length,
                    var_length=row.var_length,
                    tag_length=row.tag_length,
                    generate=row.generate,
                    reversal=row.reversal,
                    matching=row.matching,
                    alpha=row.alpha,
                    numeric=row.numeric,
                    special=row.special,
                    reserved_for_future=row.reserved_for_future,
                    description=row.description,
                    is_secret=row.is_secret,
                    fields=None
                )

                fields[row.field_number] = field

                if not(validators := self.spec.get_field_validations(field.field_path)):
                    validators = Validators()

                field.validators = validators

                if not row.childCount():
                    continue

                if not (field_object := fields.get(row.field_number)):
                    continue

                field_object.fields = generate_fields(row)

            return fields

        fields_set: FieldSet = generate_fields()

        return EpaySpecModel(
            name=name,
            fields=fields_set,
            mti=self.spec.mti
        )
