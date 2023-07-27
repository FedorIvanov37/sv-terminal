from json import loads
from pathlib import Path
from logging import error, warning, info
from pydantic import FilePath
from binascii import hexlify, unhexlify
from configparser import ConfigParser, NoSectionError, NoOptionError
from common.lib.core.EpaySpecification import EpaySpecification
from common.lib.core.Bitmap import Bitmap
from common.lib.core.FieldsGenerator import FieldsGenerator
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

    @staticmethod
    def create_dump(transaction: Transaction, body: bool = False) -> bytes | str:
        spec: EpaySpecification = EpaySpecification()
        msg_type: bytes = transaction.message_type.encode()
        bitmap: Bitmap = Bitmap(transaction.data_fields)
        bitmap: bytes = bitmap.get_bitmap(bytes)

        msg_body: bytes = bytes()

        for field in sorted(transaction.data_fields.keys(), key=int):
            if not (text := transaction.data_fields.get(field)):
                warning("No value for field %s. IsoField was ignored" % field)
                continue

            if isinstance(text, dict):
                text = Parser.join_complex_field(field, text)

            field_length_var = spec.get_field_length_var(field)

            if field_length_var:
                text_length = str(len(text)).zfill(field_length_var)
                text = f"{text_length}{text}"

            if text is not None:
                msg_body: bytes = msg_body + text.encode()

        if body:
            return msg_body.decode()

        return msg_type + bitmap + msg_body

    @staticmethod
    def create_sv_dump(transaction: Transaction) -> str | None:
        mti: str = transaction.message_type
        bitmap: hex = Bitmap(transaction.data_fields)
        bitmap: hex = bitmap.get_bitmap(hex)
        body: str = Parser.create_dump(transaction, body=True)

        # try:
        #     body: str = Parser.create_dump(transaction, body=True)
        # except Exception as exc:
        #     error("Dump generating error: %s", exc)
        #     return

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

    @staticmethod
    def join_complex_field(field, field_data, path=None):
        spec: EpaySpecification = EpaySpecification()

        if path is None:
            path = [field]

        result: str = str()
        subfield_data: str | FieldSet
        subfield: str

        for subfield, subfield_data in field_data.items():
            path.append(subfield)

            if not (subfield_spec := spec.get_field_spec(path)):
                raise ValueError(f"Lost specification for field {'.'.join(path)}! " 
                                 "Set parameters in the Specification tool. ")

            if subfield_spec.fields:
                result += Parser.join_complex_field(subfield, subfield_data, path)
            else:
                length = str(len(subfield_data))
                length = length.zfill(subfield_spec.var_length)
                result = f"{result}{subfield}{length}{subfield_data}"

            path.pop()

        if len(path) > 1:
            field_spec: IsoField = spec.get_field_spec(path)
            result = f"{field}{len(result):0{field_spec.var_length}}{result}"

        return result

    @staticmethod
    def parse_dump(data) -> Transaction:
        spec: EpaySpecification = EpaySpecification()
        fields: RawFieldSet = {}
        position = int()
        message_type_indicator = data[position:spec.MessageLength.message_type_length].decode()
        position += len(message_type_indicator)
        bitmap: str = data[position: position + spec.MessageLength.bitmap_length]
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

            if field == spec.FIELD_SET.FIELD_001_BITMAP_SECONDARY:
                continue

            length_var = spec.get_field_length_var(field)

            if length_var > 0:
                length = int(data[position:position + length_var])
                position += length_var
                fields[field] = data[position:position + length]
            else:
                length = spec.get_field_length(field)
                fields[field] = data[position:position + length]

            position += length

        for field in fields:
            if spec.is_field_complex([field]):
                try:
                    fields[field]: RawFieldSet = Parser.split_complex_field(field, fields[field])
                except ValueError:
                    raise ValueError("Incorrect transaction message or wrong Specification settings")

        transaction: Transaction = Transaction(
            trans_id=FieldsGenerator.generate_trans_id(),
            message_type=message_type_indicator,
            data_fields=fields
        )

        return transaction

    @staticmethod
    def split_complex_field(field: str, field_data: str, spec: dict | None = None) -> RawFieldSet | None:
        complex_field_data: RawFieldSet = dict()

        if spec is None:  # First entry
            spec: EpaySpecification = EpaySpecification()
            spec: IsoField = spec.get_field_spec([field])

        while field_data:
            tag_number = field_data[:spec.tag_length]
            field_data = field_data[spec.tag_length:]
            field_spec = spec.fields.get(tag_number)

            try:
                var_length = spec.tag_length

                if not var_length:
                    raise ValueError("Lost variable length")

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
                value_data = Parser.split_complex_field(tag_number, value_data, field_spec)

            complex_field_data[tag_number] = value_data

        return complex_field_data

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

    def parse_file(self, filename: FilePath) -> Transaction:
        file_extension = Path(filename).suffix
        file_extension = file_extension.replace(".", "")
        file_extension = file_extension.upper()

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
        transaction.trans_id = FieldsGenerator.generate_trans_id()
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

            if self.spec.is_field_complex([field]):
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
                    raise ValueError("Unexpected result of data parsing - no data")

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
