from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseDefinition(object):
    EMAIL = "f.ivanov@unlimit.com"
    AUTHOR = "Fedor Ivanov | Unlimit"
    VERSION = "v0.15"
    RELEASE = "Apr 2023"
    CONTACT = f'<a href="mailto:{EMAIL}?subject=SvTerminal\'s user request&body=Dear Fedor,\n\n\n' \
              f'> Put your request here < \n\n\n\n'\
              f'My SvTerminal version is {VERSION} | Released in {RELEASE}">{EMAIL}</a>'
