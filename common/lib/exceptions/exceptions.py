class BrokenConfig(Exception):  # Cannot open or read ConfigParser incoming file
    pass


class NoMandatoryData(Exception):  # The form does not contain a mandatory data
    pass


class DataIsInvalid(Exception):  # Form data invalid or incompatible with BPC e-pay protocol
    pass


class FieldError(Exception):  # Error during parsing the field - wrong length, format, etc
    pass


class FieldReservedError(Exception):  # Requested field reserved for future
    pass


class FieldDoesNotExist(Exception):  # Requested field does not exist
    pass


class InterfaceException(Exception):  # Qq exceptions
    pass


class WrongConnectionSettings(Exception):  # Lost address or port_number
    pass


class DumpFileParsingError(Exception):
    pass


class ParsingError(Exception):
    pass
