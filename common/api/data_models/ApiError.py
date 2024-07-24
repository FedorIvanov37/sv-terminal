from pydantic import BaseModel, field_validator


class ApiError(BaseModel):
    error: str = ""

    @field_validator("error", mode="before")
    @classmethod
    def exception_to_string(cls, val):
        if isinstance(val, Exception):
            return str(val)

        return val
