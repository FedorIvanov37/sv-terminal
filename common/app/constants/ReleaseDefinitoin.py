from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseDefinition:
    AUTHOR = "Fedor Ivanov | Unlimint"
    VERSION = "v0.15"
    CONTACT = "f.ivanov@unlimint.com"
    RELEASE = "Jul 2022"
    RELEASE_NOTES: str = """Release notes
# ...
# ... """
