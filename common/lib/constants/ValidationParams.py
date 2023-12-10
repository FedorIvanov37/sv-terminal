from typing import Final


MUST_CONTAIN: Final[str] = "Must contain"
MUST_CONTAIN_ONLY: Final[str] = "Must contain only"
MUST_NOT_CONTAIN: Final[str] = "Must not contain"
MUST_NOT_CONTAIN_ONLY: Final[str] = "Must not contain only"
MUST_START_WITH: Final[str] = "Must start with"
MUST_NOT_START_WITH: Final[str] = "Must not start with"
MUST_END_WITH: Final[str] = "Must end with"
MUST_NOT_END_WITH: Final[str] = "Must not end with"
VALID_VALUES: Final[str] = "Valid values"
INVALID_VALUES: Final[str] = "Invalid values"


LITERAL_VALIDATIONS: Final[tuple] = (
    MUST_CONTAIN,
    MUST_CONTAIN_ONLY,
    MUST_NOT_CONTAIN,
    MUST_NOT_CONTAIN_ONLY,
    MUST_START_WITH,
    MUST_NOT_START_WITH,
    MUST_END_WITH,
    MUST_NOT_END_WITH,
    VALID_VALUES,
    INVALID_VALUES
)
