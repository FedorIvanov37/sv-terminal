from pydantic import BaseModel, Field, field_validator


class Country(BaseModel):
    name: str
    code_a3: str = Field(..., min_length=3, max_length=3)
    code_n3: str = Field(..., min_length=3, max_length=3)
    code_a2: str = Field(..., min_length=2, max_length=2)

    @field_validator("code_a3", "code_a2", mode="before")
    @classmethod
    def non_digits_only(cls, val):
        for country in val:
            if not str(country).isalpha():
                raise ValueError("Only alphabetic allowed")

        return val

    @field_validator("code_n3", mode="before")
    @classmethod
    def digits_only(cls, val):
        for country in val:
            if not str(country).isdigit():
                raise ValueError("Only numeric codes allowed")

        return val


class Countries(BaseModel):
    countries: list[Country] = list()
