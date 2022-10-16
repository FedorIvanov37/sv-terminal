from os.path import splitext
from json import loads
from logging import error, warning, info
from binascii import hexlify, unhexlify
from configparser import ConfigParser
from common.app.exceptions.exceptions import DumpFileParsingError
from common.app.constants.DumpDefinition import DumpDefinition
from common.app.core.tools.epay_specification import EpaySpecification
from common.app.core.tools.bitmap import Bitmap
from common.app.data_models.message import Message, TransactionModel, MessageConfig
from common.app.constants.IniMessageDefinition import IniMessageDefinition
from common.app.constants.DataFormats import DataFormats
from common.app.data_models.config import Config
from common.app.data_models.epay_specification import IsoField, FieldSet, RawFieldSet
from common.app.core.tools.fields_generator import FieldsGenerator


class Parser(object):
    _spec: EpaySpecification = EpaySpecification()

    @property
    def spec(self):
        return self._spec

    def __init__(self, config: Config):
        self.config: Config = config
        self.generator = FieldsGenerator(self.config)

    def create_dump(self, message: Message, body: bool = False) -> bytes | str:
        msgtype: bytes = message.transaction.message_type.encode()
        bitmap: Bitmap = Bitmap(message.transaction.fields)
        bitmap: bytes = bitmap.get_bitmap(bytes)

        msg_body: bytes = bytes()

        for field in sorted(message.transaction.fields.keys(), key=int):
            text = message.transaction.fields.get(field)

            if not text:
                warning("No value for field %s. IsoField was ignored" % field)
                continue

            if isinstance(text, dict):
                text = self.join_complex_field(field, text)

            field_length_var = self.spec.get_field_length_var(field)

            if field_length_var:
                text: str = str(len(text)).zfill(field_length_var) + text

            if text is not None:
                msg_body: bytes = msg_body + text.encode()

        if body:
            return msg_body.decode()

        return msgtype + bitmap + msg_body

    def create_sv_dump(self, message: Message) -> str | None:
        mti: str = message.transaction.message_type
        bitmap: hex = Bitmap(message.transaction.fields)
        bitmap: hex = bitmap.get_bitmap(hex)

        try:
            body: str = self.create_dump(message, body=True)
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
                    length = str(len(subfield_data)).zfill(field_spec.tag_length)

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
            result = f"{field}{str(len(result)).zfill(field_spec.var_length)}{result}"

        return result

    def parse_dump(self, data):
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

        message: Message = Message(
            transaction=TransactionModel(
                message_type=message_type_indicator,
                fields=fields
            )
        )

        return message

    def parse_form(self, form) -> Message | None:
        if not (fields := form.get_fields()):
            error("No data to send")
            return

        if not (mti := form.get_mti()):
            error("Invalid MTI")
            return

        generate_fields = form.get_fields_to_generate()
        config = MessageConfig(generate_fields=generate_fields, max_amount=self.config.fields.max_amount)
        transaction = TransactionModel(message_type=mti, fields=fields)
        message = Message(transaction=transaction, config=config)
        return message

    def get_transaction_data_ini(self, message: Message, string: bool = False) -> ConfigParser | str:
        ini: ConfigParser = ConfigParser()

        generate_fields = ", ".join(sorted(message.config.generate_fields, key=int))

        ini_data = [
            (IniMessageDefinition.CONFIG, IniMessageDefinition.MAX_AMOUNT, message.config.max_amount),
            (IniMessageDefinition.CONFIG, IniMessageDefinition.GENERATE_FIELDS, generate_fields),
            (IniMessageDefinition.MTI, IniMessageDefinition.MTI, message.transaction.message_type)
        ]

        for field, field_data in message.transaction.fields.items():
            if isinstance(field_data, dict):
                field_data = self.join_complex_field(field, field_data)

            field_data = field_data.replace("%", "%%")
            ini_data.append((IniMessageDefinition.MESSAGE, "F" + field.zfill(3), field_data))

        for section, option, value in ini_data:
            if section not in ini.sections():
                ini.add_section(section)

            value = "[%s]" % value
            ini.set(section, option, value)

        if string:
            ini: str = self.ini_to_string(ini)

        return ini

    @staticmethod
    def ini_to_string(ini: ConfigParser) -> str:
        result: str = str()

        for section in ini.sections():
            result += f"[{section}]\n"

            for option in ini.options(section):
                value = ini.get(section, option)
                result += f"{option} = {value}\n"

        result: str = result.replace("%", "%%")

        return result

    def split_complex_field(self, field: str, field_data: str, spec: dict | None = None) -> RawFieldSet | None:
        complex_field_data: RawFieldSet = dict()

        if spec is None:  # First entry
            spec = self.spec.get_field_spec([field])

        while field_data:
            tag_number = field_data[:spec.tag_length]
            field_data = field_data[spec.tag_length:]
            field_spec = spec.fields.get(tag_number)

            try:
                variable_length = spec.tag_length

                if not variable_length:
                    raise ValueError

            except(AttributeError, ValueError):
                error("Lost specification for field %s ", field)
                error("The field and corresponding sub fields were absent")
                return {}

            variable_length = spec.tag_length
            val_length = field_data[:variable_length]
            val_length = int(val_length)
            field_data = field_data[variable_length:]
            value_data = field_data[:val_length]
            field_data = field_data[val_length:]

            if field_spec and field_spec.fields:
                value_data = self.split_complex_field(tag_number, value_data, field_spec)

            complex_field_data[tag_number] = value_data

        return complex_field_data

    def parse_file(self, filename: str) -> Message:
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
    def _parse_json_file(filename: str) -> Message:
        message: Message = Message.parse_file(filename)
        return message

    def _parse_ini_file(self, filename):
        def unpack(data: str) -> str:
            return data.removeprefix('[').removesuffix(']')

        ini = ConfigParser()
        ini.read(filename)

        fields = dict()

        for option in ini.options(IniMessageDefinition.MESSAGE):
            if not option.startswith("f"):
                error("Wrong field name: %s. Should start from f. For example: f002", option)
                return

            field = str(int(option.removeprefix("f")))
            value = unpack(ini.get(IniMessageDefinition.MESSAGE, option))

            if self.spec.is_field_complex(field):
                value = self.split_complex_field(field, value)

            fields[field] = value

        max_amount = self.config.fields.max_amount
        generate_fields = list()

        if IniMessageDefinition.CONFIG in ini.sections():
            options = list(option.upper() for option in ini.options(IniMessageDefinition.CONFIG))

            if IniMessageDefinition.MAX_AMOUNT.upper() in options:
                max_amount = int(unpack(ini.get(IniMessageDefinition.CONFIG, IniMessageDefinition.MAX_AMOUNT)))

            if IniMessageDefinition.GENERATE_FIELDS.upper() in options:
                generate_fields = loads(ini.get(IniMessageDefinition.CONFIG, IniMessageDefinition.GENERATE_FIELDS))

        message_config = MessageConfig(
            generate_fields=generate_fields,
            max_amount=max_amount
        )

        transaction = TransactionModel(
            message_type=unpack(ini.get(IniMessageDefinition.MTI, IniMessageDefinition.MTI)),
            fields=fields
        )

        message = Message(
            config=message_config,
            transaction=transaction
        )

        return message

    def _parse_dump_file(self, filename: str) -> Message:
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
        message: Message = self.parse_dump(pre_message)
        return message
