from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.EpaySpecificationModel import EpaySpecModel
from common.gui.constants.SpecFieldDef import SpecFieldDefinition
from common.gui.core.SpecItem import SpecItem
from common.lib.data_models.EpaySpecificationModel import IsoField, FieldSet
from common.gui.core.SpecValidator import SpecValidator


class SpecView(QObject):
    _spec: EpaySpecification = EpaySpecification()
    item_changed = pyqtSignal(SpecItem, int)
    status_changed = pyqtSignal(str, bool)

    @property
    def spec(self):
        return self._spec

    def __init__(self, tree: QTreeWidget, window):
        super(SpecView, self).__init__()

        print("INIT SPEC")

        self.root: SpecItem = SpecItem(["Specification"])
        self.tree: QTreeWidget = tree
        self.window = window
        self.validator = SpecValidator()
        self.setup()

    def setup(self):
        self.tree.setHeaderLabels(SpecFieldDefinition.COLUMNS)
        self.tree.addTopLevelItem(self.root)
        self.tree.itemDoubleClicked.connect(self.edit)
        self.tree.itemPressed.connect(lambda item, column: self.validate_item(item, column, validate_all=True))
        self.tree.itemChanged.connect(lambda item, column: self.validate_item(item, column))
        self.tree.setSortingEnabled(False)
        self.parse_spec()
        self.make_order()

    def validate_item(self, item: SpecItem, column: int, validate_all=False):
        if item is self.root:
            return

        self.set_field_path(item)

        try:
            if validate_all:
                self.validator.validate_spec_row(item)

            else:
                self.validator.validate_column(item, column)

        except ValueError as validation_error:
            self.status_changed.emit(str(validation_error), True)

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

    def clean(self):
        self.root.takeChildren()

    def resize_all(self):
        for column in range(self.tree.columnCount()):
            self.tree.resizeColumnToContents(column)

    def make_order(self):
        self.tree.collapseAll()
        self.tree.expandToDepth(int())
        self.resize_all()
        self.hide_reserved()

    def edit(self, item, column):
        if item is self.root and column != SpecFieldDefinition.ColumnsOrder.DESCRIPTION:
            return

        if column > SpecFieldDefinition.ColumnsOrder.TAG_LENGTH:
            return

        if self.window.read_only:
            self.window.set_status("Read only mode", error=True)
            return

        self.tree.editItem(item, column)

    def set_field_path(self, item):
        path = item.get_field_path(string=True)

        if not path:
            path = str()

        self.status_changed.emit(path, False)

    def minus(self):
        item: SpecItem = self.tree.currentItem()

        if item is None:
            return

        if item is self.root:
            self.tree.setCurrentItem(self.root)
            self.tree.setFocus()
            return

        self.tree.setFocus()
        parent: SpecItem = item.parent()
        parent.takeChild(parent.indexOfChild(item))

    def plus(self):
        item = SpecItem([])

        if not (current_item := self.tree.currentItem()):
            return

        parent = current_item.parent()

        if parent is None:
            return

        current_index = parent.indexOfChild(current_item)
        parent.insertChild(current_index + 1, item)
        self.tree.scrollToItem(item)
        self.edit(item, 0)
        self.tree.setCurrentItem(item)

    def next_level(self):
        item = SpecItem([])
        current_item: SpecItem = self.tree.currentItem()

        if current_item is None:
            return

        self.tree.currentItem().addChild(item)
        self.tree.setCurrentItem(item)
        self.edit(item, int())

    def parse_spec(self, spec=None):
        if spec is None:
            spec = self.spec

        self.clean()
        self.root.setText(SpecFieldDefinition.ColumnsOrder.DESCRIPTION, spec.name)
        self.parse_spec_fields(spec.fields)

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
                str(field_data.min_length),
                str(field_data.max_length),
                str(field_data.var_length),
                str(field_data.tag_length),
            ]

            checkboxes: dict[str, bool] = {
                SpecFieldDefinition.ColumnsOrder.USE_FOR_MATCHING: field_data.matching,
                SpecFieldDefinition.ColumnsOrder.USE_FOR_REVERSAL: field_data.reversal,
                SpecFieldDefinition.ColumnsOrder.CAN_BE_GENERATED: field_data.generate,
                SpecFieldDefinition.ColumnsOrder.ALPHA: field_data.alpha,
                SpecFieldDefinition.ColumnsOrder.NUMERIC: field_data.numeric,
                SpecFieldDefinition.ColumnsOrder.SPECIAL: field_data.special,
            }

            item: SpecItem = SpecItem(field_data_for_item, checkboxes=checkboxes)

            parent.addChild(item)

            if field_data.fields:
                self.parse_spec_fields(input_json=field_data.fields, parent=item)

        self.make_order()

    def generate_spec(self):
        name: str = self.root.text(SpecFieldDefinition.ColumnsOrder.DESCRIPTION)
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
                    fields=None
                )

                fields[row.field_number] = field

                if row.childCount():
                    fields[row.field_number].fields = generate_fields(row)

            return fields

        fields_set: FieldSet = generate_fields()

        return EpaySpecModel(
            name=name,
            fields=fields_set,
            mti=self.spec.mti
        )

