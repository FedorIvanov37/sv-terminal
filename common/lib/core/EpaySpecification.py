from copy import deepcopy
from dataclasses import asdict
from pydantic import FilePath
from common.lib.decorators.singleton import singleton
from common.lib.constants import MessageLength, TermFilesPath
from common.lib.constants.EpaySpecificationData import EpaySpecificationData
from common.lib.data_models.EpaySpecificationModel import EpaySpecModel, Mti, IsoField, FieldSet
from common.lib.data_models.Types import FieldPath


@singleton
class EpaySpecification(EpaySpecificationData):
    _MessageLength: MessageLength = MessageLength
    _specification_model: EpaySpecModel = None

    def __init__(self, filename: FilePath | None = None):
        if filename is None:
            filename: FilePath = TermFilesPath.SPECIFICATION

        self.filename: FilePath = filename

        with open(filename) as json_file:
            self._specification_model: EpaySpecModel = EpaySpecModel.model_validate_json(json_file.read())

    @property
    def spec(self) -> EpaySpecModel:
        return self._specification_model

    @property
    def mti(self) -> list[Mti]:
        return self.spec.mti

    @property
    def name(self):
        return self.spec.name

    @property
    def fields(self):
        return self.spec.fields

    @property
    def MessageLength(self):
        return self._MessageLength

    def is_reversal(self, mti: str):
        return mti in (
            self.MESSAGE_TYPE_INDICATORS.REVERSAL_REQUEST,
            self.MESSAGE_TYPE_INDICATORS.REVERSAL_RESPONSE,
            self.MESSAGE_TYPE_INDICATORS.REVERSAL_ADVICE_REQUEST,
            self.MESSAGE_TYPE_INDICATORS.REVERSAL_ADVICE_RESPONSE
        )

    def is_secret(self, path: FieldPath) -> bool:
        spec = self.spec

        for field in path:
            if not (spec := spec.fields.get(field)):
                return False

        return spec.is_secret

    def get_generated_fields_dict(self):
        return {field.description: field.field_number for field in self.spec.fields.values() if field.generate}

    def get_reversal_mti(self, original_mti: str):
        for mti in self.spec.mti:
            if not (mti.reversal_mti and mti.is_reversible):
                continue

            if mti.request == original_mti:
                return mti.reversal_mti

    def get_fields_to_generate(self):
        return [field for field in self.spec.fields if self.spec.fields.get(field).generate]

    def can_be_generated(self, field_path: FieldPath):
        if not (field_spec := self.get_field_spec(field_path)):
            return False

        return field_spec.generate

    def get_field_description(self, field_path: FieldPath, string: bool = False) -> str | FieldPath:
        description: list[str] = list()
        spec_fields: FieldSet = deepcopy(self.spec.fields)

        for field in field_path:
            if not (field_spec := spec_fields.get(field)):
                break

            description.append(field_spec.description)

            if not (spec_fields := field_spec.fields):
                break

        if not string:
            return description

        return ' / '.join(description)

    def get_mti_codes(self) -> list[str]:
        message_type_identifiers: set[str] = set()

        message_type: Mti

        for message_type in self.spec.mti:
            [message_type_identifiers.add(mti) for mti in (message_type.request, message_type.response)]

        message_type_identifiers: list[str] = list(message_type_identifiers)

        return message_type_identifiers

    def get_resp_mti(self, request_mti):
        for message_type_identifier in self.spec.mti:
            if message_type_identifier.request != request_mti:
                continue

            return message_type_identifier.response

    def get_mti_list(self) -> list[str]:
        message_type_desc: list[str] = []

        for message_type in self.spec.mti:
            message_type_desc.append(f"{message_type.request}: {message_type.description} Request")
            message_type_desc.append(f"{message_type.response}: {message_type.description} Response")

        return message_type_desc

    def reload_spec(self, spec: EpaySpecModel, commit: bool):
        self.spec.fields = spec.fields
        self.spec.name = spec.name

        if not commit:
            return

        with open(self.filename, "w") as spec_file:
            spec_file.write(self.spec.model_dump_json(indent=4))

    def get_reversal_fields(self):
        return (field for field, value in self.fields.items() if value.reversal)

    def get_match_fields(self):
        return [field for field, field_data in self.fields.items() if field_data.matching]

    def is_request(self, transaction):
        if not transaction.message_type:
            return False

        for mti in self.mti:
            if transaction.message_type == mti.request:
                return True

            if transaction.message_type == mti.response:
                return False

        return False

    def get_field_spec(self, path: FieldPath, spec=None) -> IsoField | None:
        if spec is None:
            spec = self.spec

        field_data = None

        for field in path:
            try:
                field_data = spec.fields.get(str(field))
            except AttributeError:
                return

            spec = field_data

        return field_data

    def is_field_complex(self, field_path: FieldPath):
        if not (field_spec := self.get_field_spec(field_path)):
            return False

        return bool(field_spec.fields)

    def get_field_length_var(self, field):
        field_spec = self.get_field_spec([field])

        if field_spec is not None:
            return field_spec.var_length

    def get_field_length(self, field):
        field_spec: IsoField = self.get_field_spec([field])

        if field is not None:
            return field_spec.max_length

    def get_field_date_format(self, field):
        for field_name, field_number in asdict(self.FIELD_SET).items():
            if field_number != field:
                continue

            return getattr(self.FIELD_DATE_FORMAT, field_name, "")

    def get_field_data_kit(self, field_path: FieldPath):
        field_spec: IsoField

        if not (field_spec := self.get_field_spec(field_path)):
            raise ValueError("Lost field spec for field %s" % ".".join(field_path))

        data_map: dict[str, bool] = {
            self.DATA_TYPES.FIELD_TYPE_ALPHA: field_spec.alpha,
            self.DATA_TYPES.FIELD_TYPE_NUMERIC: field_spec.numeric,
            self.DATA_TYPES.FIELD_TYPE_SPECIAL: field_spec.special
        }

        field_data_kit: str = str()

        for field_type, checked in data_map.items():
            if not checked:
                continue

            field_data_kit += getattr(self.FIELD_DATA_KIT, field_type, "")

        return field_data_kit
