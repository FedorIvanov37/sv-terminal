from json import dumps
from logging import error
from pydantic import ValidationError
from dataclasses import asdict
from common.app.constants.MessageLength import MessageLength
from common.app.decorators.singleton import singleton
from common.app.constants.FilePath import FilePath
from common.app.data_models.epay_specification import EpaySpecModel, Mti, IsoField
from common.app.constants.EpaySpecificationData import EpaySpecificationData


@singleton
class EpaySpecification(EpaySpecificationData):
    _MessageLength: MessageLength = MessageLength()

    try:
        _specification_model: EpaySpecModel = EpaySpecModel.parse_file(FilePath.SPECIFICATION)
    except ValidationError as JsonParsingError:
        error(f"Critical error! Cannot parse Specification: {JsonParsingError.json()}")

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

    @staticmethod
    def is_reversal(mti: str):
        if mti in ("0400", "0410", "0420", "0430"):
            return True

        return False

    def get_reversal_mti(self, original_mti: str):
        for mti in self.spec.mti:
            if not (mti.reversal_mti and mti.is_reversible):
                continue

            if mti.request == original_mti:
                return mti.reversal_mti

    def can_be_generated(self, field_path: list[str]):
        if not (field_spec := self.get_field_spec(field_path)):
            return False

        return field_spec.generate

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

        with open(FilePath.SPECIFICATION, "w") as spec_file:
            spec_file.write(dumps(self.spec.dict(), indent=4))

    def get_reversal_fields(self):
        return (field for field, value in self.fields.items() if value.reversal)

    def get_match_fields(self):
        return [field for field, field_data in self.fields.items() if field_data.matching]

    def get_field_description(self, path: list[str]) -> str | None:
        field_spec: IsoField = self.get_field_spec(path)

        try:
            return field_spec.description
        except AttributeError:
            return ""

    def is_request(self, transaction):
        if not transaction.message_type:
            return

        for mti in self.mti:
            if transaction.message_type == mti.request:
                return True

            if transaction.message_type == mti.response:
                return False

    def get_field_spec(self, path: list[str], spec=None) -> IsoField | None:
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

    def is_field_complex(self, field):
        field_spec = self.get_field_spec([field])

        if field_spec is None:
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

    def get_field_data_kit(self, field_path: list[str]):
        field_spec: IsoField = self.get_field_spec(field_path)

        if not field_spec:
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
