from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QTreeWidgetItem, QItemDelegate
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.data_models.EpaySpecificationModel import EpaySpecModel
from common.lib.data_models.EpaySpecificationModel import IsoField, FieldSet
from common.gui.constants.SpecFieldDef import SpecFieldDefinition
from common.gui.core.json_items.SpecItem import SpecItem
from common.gui.core.validators.SpecValidator import SpecValidator
from common.gui.decorators.void_qt_signals import void_qt_signals
from common.gui.core.json_views.TreeView import TreeView
from common.gui.constants.Colors import Colors


class SpecView(TreeView):
    _spec: EpaySpecification = EpaySpecification()
    item_changed = pyqtSignal(SpecItem, int)
    status_changed = pyqtSignal(str, bool)
    search_finished = pyqtSignal()

    @property
    def spec(self):
        return self._spec

    def __init__(self, window):
        super(SpecView, self).__init__()
        self.root: SpecItem = SpecItem([SpecFieldDefinition.SPECIFICATION])
        self.window = window
        self.validator = SpecValidator()
        self.setItemDelegate(QItemDelegate())
        self._setup()

    def _setup(self):
        self.setHeaderLabels(SpecFieldDefinition.COLUMNS)
        self.addTopLevelItem(self.root)
        self.itemDoubleClicked.connect(self.edit_item)
        self.itemPressed.connect(lambda item, column: self.validate_item(item, column, validate_all=True))
        self.itemChanged.connect(self.process_item_change)
        self.currentItemChanged.connect(self.set_path_status)
        self.parse_spec()
        self.make_order()
        self.collapseAll()
        self.root.setExpanded(True)
        self.resizeColumnToContents(SpecFieldDefinition.ColumnsOrder.DESCRIPTION)

    def set_path_status(self):
        item: SpecItem

        if not (item := self.currentItem()):
            return

        if not (path := item.get_field_path(string=True)):
            return

        path = f"{path} {item.description}"

        self.status_changed.emit(path, False)

    def process_item_change(self, item, column):
        if item.field_number == self.spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
            self.set_pan_as_secret(item)

        if column == SpecFieldDefinition.ColumnsOrder.SECRET:
            self.cascade_checkboxes(item)

        if column == SpecFieldDefinition.ColumnsOrder.TAG_LENGTH:
            self.cascade_tag_length(item)

        self.validate_item(item, column, validate_all=True)

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
        check_state = parent.checkState(SpecFieldDefinition.ColumnsOrder.SECRET)

        for item in parent.get_children():
            item.setCheckState(SpecFieldDefinition.ColumnsOrder.SECRET, check_state)

            if item.childCount():
                self.cascade_checkboxes(item)

    def set_pan_as_secret(self, item: SpecItem):
        if item.field_number != self.spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
            return

        item.setCheckState(SpecFieldDefinition.ColumnsOrder.SECRET, Qt.CheckState.PartiallyChecked)

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

    def edit_item(self, item, column):
        if item is self.root and column != SpecFieldDefinition.ColumnsOrder.DESCRIPTION:
            return

        if column > SpecFieldDefinition.ColumnsOrder.TAG_LENGTH:
            return

        if self.window.read_only:
            self.window.set_status("Read only mode", error=True)
            return

        self.editItem(item, column)

    def set_field_path(self, item):
        try:
            if not (path := item.get_field_path(string=True)):
                path = str()

            path = f"{path} {item.description}"

        except AttributeError:
            path = str()

        self.status_changed.emit(path, False)

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
        self.edit_item(item, 0)
        self.setCurrentItem(item)

    def next_level(self):
        item = SpecItem([])
        current_item: SpecItem = self.currentItem()

        if current_item is None:
            return

        self.currentItem().addChild(item)
        self.setCurrentItem(item)
        self.edit_item(item, int())

    def parse_spec(self, spec=None):
        if spec is None:
            spec = self.spec

        self.clean()
        self.root.setText(SpecFieldDefinition.ColumnsOrder.DESCRIPTION, spec.name)
        self.parse_spec_fields(spec.fields)
        self.collapseAll()
        self.expandItem(self.root)

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
                SpecFieldDefinition.ColumnsOrder.SECRET: field_data.is_secret
            }

            item: SpecItem = SpecItem(field_data_for_item, checkboxes=checkboxes)

            if item.field_number == self.spec.FIELD_SET.FIELD_002_PRIMARY_ACCOUNT_NUMBER:
                self.set_pan_as_secret(item)

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
                    is_secret=row.is_secret,
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
