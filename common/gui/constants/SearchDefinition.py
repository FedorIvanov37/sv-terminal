from dataclasses import dataclass


@dataclass
class SearchDefinition:
    PATH_SEPARATOR_DOT = '.'
    PATH_SEPARATOR_SLASH = '/'
    FIELD_PATH_PATTERN = "^(?:\d+(\.|/)?)+$"
