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

    class MessageTypeSpec:
        _spec: EpaySpecModel = EpaySpecModel.parse_file(FilePath.SPECIFICATION)

        @property
        def spec(self):
            return self._spec

        @property
        def message_types_description(self) -> dict[str, str]:
            desc: dict[str, str] = {}
            mti: Mti

            for mti in self.spec.mti:
                desc[mti.request] = mti.description + " Request"  # TODO raw strings
                desc[mti.response] = mti.description + " Response"  # TODO raw strings

            return desc

        @property
        def reversible_messages(self):
            return [mti.request for mti in self.spec.mti if mti.is_reversible]

        def get_desc(self, mti):
            try:
                return self.message_types_description[mti]
            except KeyError:
                return str()

        def get_mti_list(self):
            message_types = list()

            for message_type, desc in self.message_types_description.items():
                message_types.append(f"{message_type}: {desc}")

            return message_types

        def get_mti_codes(self):
            mti_codes: set[str] = set()

            for mti in self.get_mti_list():
                mti_codes.add(mti[:MessageLength.message_type_length])

            return list(mti_codes)

        def get_resp_mti(self, request_mti):
            for mti in self.spec.mti:
                if mti.request == request_mti:
                    return mti.response

        def is_reversible(self, mti):
            return mti in self.reversible_messages

    try:
        _specification_model: EpaySpecModel = EpaySpecModel.parse_file(FilePath.SPECIFICATION)
        _MessageTypeSpec: MessageTypeSpec = MessageTypeSpec()
        _MessageLength = MessageLength()
    except ValidationError as JsonParsingError:
        error(f"Specification JSON parsing error: {JsonParsingError.json()}")
        raise JsonParsingError

    @property
    def spec(self):
        return self._specification_model

    @property
    def mti(self):
        return self.spec.mti

    @mti.setter
    def mti(self, mti: list[Mti]):
        self.spec.mti = mti

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
    def get_internal_id_path() -> list[str]:  # TODO hardcode
        return ["47", "072"]

    @staticmethod
    def get_utrnno_path():  # TODO hardcode
        return ["47", "064"]

    @property
    def message_types_description(self) -> dict[str, str]:
        return self._MessageTypeSpec.message_types_description

    @property
    def reversible_messages(self):
        return self._MessageTypeSpec.reversible_messages

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

    def get_reversal_mti(self, request_mti):
        for mti in self.spec.mti:
            if not mti.reversal_mti or not mti.is_reversible:
                continue

            if mti.request == request_mti:
                return mti.reversal_mti

    def get_desc(self, mti):
        return self._MessageTypeSpec.get_desc(mti)

    def get_mti_list(self):
        return self._MessageTypeSpec.get_mti_list()

    def get_mti_codes(self):
        return self._MessageTypeSpec.get_mti_codes()

    def get_resp_mti(self, request_mti):
        return self._MessageTypeSpec.get_resp_mti(request_mti)

    def is_reversible(self, mti):
        return self._MessageTypeSpec.is_reversible(mti)
