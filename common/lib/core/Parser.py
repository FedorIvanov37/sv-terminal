from json import loads
from os.path import splitext
from logging import error, warning, info
from pydantic import FilePath
from binascii import hexlify, unhexlify
from configparser import ConfigParser, NoSectionError, NoOptionError
from common.lib.exceptions.exceptions import DumpFileParsingError
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.core.Bitmap import Bitmap
from common.lib.toolkit.trans_id import trans_id
from common.lib.constants.DumpDefinition import DumpDefinition
from common.lib.constants.IniMessageDefinition import IniMessageDefinition
from common.lib.constants.DataFormats import DataFormats
from common.lib.data_models.Config import Config
from common.lib.data_models.EpaySpecificationModel import IsoField, FieldSet, RawFieldSet
from common.lib.data_models.Transaction import TypeFields, Transaction


class Parser:
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    def __init__(self, config: Config):
        self.config: Config = config

    def create_dump(self, transaction: Transaction, body: bool = False) -> bytes | str:
        msg_type: bytes = transaction.message_type.encode()
        bitmap: Bitmap = Bitmap(transaction.data_fields)
        bitmap: bytes = bitmap.get_bitmap(bytes)

        msg_body: bytes = bytes()

        for field in sorted(transaction.data_fields.keys(), key=int):
            if not (text := transaction.data_fields.get(field)):
                warning("No value for field %s. IsoField was ignored" % field)
                continue

            if isinstance(text, dict):
                text = self.join_complex_field(field, text)

            field_length_var = self.spec.get_field_length_var(field)

            if field_length_var:
                text: str = f"{len(text):0{field_length_var}}{text}"

            if text is not None:
                msg_body: bytes = msg_body + text.encode()

        if body:
            return msg_body.decode()

        return msg_type + bitmap + msg_body

    def create_sv_dump(self, transaction: Transaction) -> str | None:
        mti: str = transaction.message_type
        bitmap: hex = Bitmap(transaction.data_fields)
        bitmap: hex = bitmap.get_bitmap(hex)

        try:
            body: str = self.create_dump(transaction, body=True)
        except Exception as exc:
            error("Dump generating error: %s", exc)
            return

        dump = "\n"
        ascii_dump = mti + DumpDefinition.ASCII_BITMAP + body
        hex_dump = hexlify(mti.encode()).decode() + bitmap + hexlify(body.encode()).decode().upper()

        for position in range(0, len(hex_dump), DumpDefinition.LINE_LENGTH):
            sub_string = str()
            string = hex_dump[position:position + DumpDefinition.LINE_LENGTH]

            for sub_position in range(0, len(string), DumpDefinition.BYTE_LENGTH):
                sub_string += string[sub_position:sub_position + DumpDefinition.BYTE_LENGTH]
                sub_string += DumpDefinition.SEPARATOR

            sub_string = sub_string[:-1]
            sub_string = sub_string.ljust(DumpDefinition.HEX_LINE_LENGTH, " ")
            position = int(position / 2)
            sub_string += ascii_dump[position:position + DumpDefinition.ASCII_LINE_LENGTH]
            sub_string += "\n"
            dump += sub_string

        return dump

    def join_complex_field(self, field, field_data, path=None):
        if path is None:
            path = [field]

        result: str = str()
        subfield_data: str | FieldSet
        subfield: str

        for subfield, subfield_data in field_data.items():
            path.append(subfield)
            subfield_spec = self.spec.get_field_spec(path)

            if subfield_spec is None:
                warning("Lost specification for field %s! Set parameters in the Specification tool", ".".join(path))
                field_spec: IsoField = self.spec.get_field_spec(path[:-1])

                length = str()

                if field_spec:
                    length = f"{len(subfield_data)}:0{field_spec.tag_length}"

                result += f"{subfield}{length}{subfield_data}"
                path.pop()
                continue

            if subfield_spec.fields:
                result += self.join_complex_field(subfield, subfield_data, path)
            else:
                length = str(len(subfield_data))
                length = length.zfill(subfield_spec.var_length)
                result = f"{result}{subfield}{length}{subfield_data}"

            path.pop()

        if len(path) > 1:
            field_spec: IsoField = self.spec.get_field_spec(path)
            result = f"{field}{len(result):0{field_spec.var_length}}{result}"

        return result

    def parse_dump(self, data) -> Transaction:
        fields: RawFieldSet = {}
        position = int()
        message_type_indicator = data[position:self.spec.MessageLength.message_type_length].decode()
        position += len(message_type_indicator)
        bitmap: str = data[position: position + self.spec.MessageLength.bitmap_length]
        position += len(bitmap)
        second_bitmap_exists = Bitmap(bitmap, bytes).second_bitmap_exists()

        if second_bitmap_exists:
            length = len(bitmap)
            bitmap += data[position: position + length]
            position += length

        data = data[position:].decode()
        position = 0
        bitmap: Bitmap = Bitmap(bitmap, bytes)
        bitmap: dict[str, bool] = bitmap.get_bitmap(dict)

        for field, exists in bitmap.items():
            if not exists:
                continue

            if field == self.spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY:
                continue

            length_var = self.spec.get_field_length_var(field)

            if length_var > 0:
                length = int(data[position:position + length_var])
                position += length_var
                fields[field] = data[position:position + length]
            else:
                length = self.spec.get_field_length(field)
                fields[field] = data[position:position + length]

            position += length

        for field in fields:
            if self.spec.is_field_complex(field):
                fields[field]: RawFieldSet = self.split_complex_field(field, fields[field])

        transaction: Transaction = Transaction(
            trans_id=trans_id(),
            message_type=message_type_indicator,
            data_fields=fields
        )

        return transaction

    def parse_main_window(self, form) -> Transaction:
        data_fields: TypeFields = form.get_fields()

        if not data_fields:
            raise ValueError("No data to send")

        if not (message_type := form.get_mti()):
            raise ValueError("Invalid MTI")

        message_type = message_type[:self.spec.MessageLength.message_type_length]
        generate_fields = form.get_fields_to_generate()
        max_amount = self.config.fields.max_amount

        transaction = Transaction(
            trans_id=trans_id(),
            message_type=message_type,
            max_amount=max_amount,
            generate_fields=generate_fields,
            data_fields=data_fields
        )

        return transaction

    def transaction_to_ini_string(self, transaction: Transaction):
        generate_fields: list[str] = sorted(transaction.generate_fields, key=int)
        generate_fields: str = ", ".join(generate_fields)

        ini_data: list[str] | str = [
            f"[{IniMessageDefinition.CONFIG}]",
            f"{IniMessageDefinition.MAX_AMOUNT} = [{transaction.max_amount}]",
            f"{IniMessageDefinition.GENERATE_FIELDS} = [{generate_fields}]",
            f"[{IniMessageDefinition.MTI}]",
            f"{IniMessageDefinition.MTI} = [{transaction.message_type}]",
            f"[{IniMessageDefinition.MESSAGE}]"
        ]

        for field_number, field_data in transaction.data_fields.items():
            if isinstance(field_data, dict):
                field_data = self.join_complex_field(field_number, field_data)

            field_data = field_data.replace("%", "%%")

            try:
                field_number = f"F{int(field_number):03}"
            except ValueError:
                error(f"Wrong field number {field_number}")

            ini_data.append(f"{field_number} = [{field_data}]")

        ini_data = "\n".join(ini_data)

        return ini_data

    def split_complex_field(self, field: str, field_data: str, spec: dict | None = None) -> RawFieldSet | None:
        complex_field_data: RawFieldSet = dict()

        if spec is None:  # First entry
            spec = self.spec.get_field_spec([field])

        while field_data:
            tag_number = field_data[:spec.tag_length]
            field_data = field_data[spec.tag_length:]
            field_spec = spec.fields.get(tag_number)

            try:
                var_length = spec.tag_length

                if not var_length:
                    raise ValueError

            except(AttributeError, ValueError):
                error("Lost specification for field %s ", field)
                error("The field and corresponding sub fields were absent")
                return {}

            var_length = spec.tag_length
            val_length = field_data[:var_length]
            val_length = int(val_length)
            field_data = field_data[var_length:]
            value_data = field_data[:val_length]
            field_data = field_data[val_length:]

            if field_spec and field_spec.fields:
                value_data = self.split_complex_field(tag_number, value_data, field_spec)

            complex_field_data[tag_number] = value_data

        return complex_field_data

    def parse_file(self, filename: FilePath) -> Transaction:
        file_extension = splitext(filename)[-1].upper().replace(".", "")

        data_processing_map = {
            DataFormats.JSON: self._parse_json_file,
            DataFormats.INI: self._parse_ini_file,
            DataFormats.TXT: self._parse_dump_file
        }

        if function := data_processing_map.get(file_extension):
            return function(filename)

        warning("Unknown file extension, trying to guess the format")

        for extension in data_processing_map:
            info(f"Trying to parse file as {extension}")
            function = data_processing_map.get(extension)

            try:
                return function(filename)

            except Exception as parsing_error:
                warning(f"Cannot parse file as {extension}: {parsing_error}")
                continue

        raise TypeError("Can't parse incoming file using known formats")

    @staticmethod
    def _parse_json_file(filename: str) -> Transaction:
        transaction: Transaction = Transaction.parse_file(filename)
        transaction.trans_id = trans_id()
        return transaction

    @staticmethod
    def unpack_ini_field(data: str) -> str:
        return data.removeprefix('[').removesuffix(']')

    def _parse_ini_file(self, filename) -> Transaction:
        ini = ConfigParser()
        ini.read(filename)
        fields: TypeFields = self._parse_ini_fields(ini)

        ini_def = IniMessageDefinition

        try:
            max_amount = ini.get(ini_def.CONFIG, ini_def.MAX_AMOUNT)
            max_amount = self.unpack_ini_field(max_amount)
        except (NoSectionError, NoOptionError):
            max_amount = self.config.fields.max_amount

        try:
            generate_fields = loads(ini.get(ini_def.CONFIG, ini_def.GENERATE_FIELDS))
        except(NoSectionError, NoOptionError):
            generate_fields: list[str] = []

        mti = self.unpack_ini_field(ini.get(ini_def.MTI, ini_def.MTI))

        transaction = Transaction(
            message_type=mti,
            generate_fields=generate_fields,
            max_amount=max_amount,
            data_fields=fields
        )

        return transaction

    def _parse_ini_fields(self, ini: ConfigParser):
        fields: RawFieldSet = dict()

        for option in ini.options(IniMessageDefinition.MESSAGE):
            if not option.startswith("f"):
                raise ValueError("Wrong field name: %s. Should start from f. For example: f002", option)

            field = str(int(option.removeprefix("f")))
            value = self.unpack_ini_field(ini.get(IniMessageDefinition.MESSAGE, option))

            if self.spec.is_field_complex(field):
                value = self.split_complex_field(field, value)

            fields[field] = value

        return fields

    def _parse_dump_file(self, filename: str) -> Transaction:
        string = str()

        with open(filename) as file:
            for line in file.readlines():
                if not line.replace(" ", "").replace("\n", ""):
                    continue

                try:
                    line = line.split()[0]
                except IndexError:
                    raise DumpFileParsingError("Unexpected result of data parsing - no data")

                line = line.replace(DumpDefinition.SEPARATOR, "")
                string += line

        mti = string[:self.spec.MessageLength.message_type_length * 2]
        string = string[len(mti):]
        bitmap = string[:self.spec.MessageLength.first_bitmap_length_hex]
        string = string[len(bitmap):]
        bitmap = Bitmap(bitmap, hex).get_bitmap(bytes)
        pre_message = unhexlify(mti) + bitmap + unhexlify(string)
        transaction: Transaction = self.parse_dump(pre_message)

        return transaction
