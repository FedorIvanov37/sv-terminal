from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseDefinition(object):
    EMAIL = "f.ivanov@unlimint.com"
    AUTHOR = "Fedor Ivanov | Unlimint"
    VERSION = "v0.15"
    RELEASE = "Apr 2023"
    CONTACT = f'<a href="mailto:{EMAIL}'\
              f'?subject=SvTerminal\'s user request&body=\n\nSvTerminal {VERSION} | Released in {RELEASE}">{EMAIL}</a>'
