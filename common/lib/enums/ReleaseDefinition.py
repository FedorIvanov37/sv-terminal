from enum import StrEnum


class ReleaseDefinition(StrEnum):
    EMAIL = "fedornivanov@gmail.com"
    AUTHOR = "Fedor Ivanov"
    VERSION = "v0.18"
    VERSION_NUMBER = "18"
    NAME = "signal"
    RELEASE = "May 2024"
    CONTACT = (f"<a href=\"mailto:{EMAIL}?subject=SIGNAL's user request&body=Dear Fedor,\n\n\n"
               f"> Put your request here < \n\n\n\n"
               f"My SIGNAL version is {VERSION} | Released in {RELEASE}\">{EMAIL}</a>")
