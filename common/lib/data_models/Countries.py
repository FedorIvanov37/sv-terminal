from pydantic import BaseModel, field_validator


class Countries(BaseModel):
    countries_a3: list[str] = list()
    countries_a2: list[str] = list()
    countries_n3: list[str] = list()

    @field_validator("countries_a2", "countries_a3", mode="before")
    @classmethod
    def non_digits_only(cls, val):
        for country in val:
            if not str(country).isalpha():
                raise ValueError("Only alphabetic allowed")

        return val

    @field_validator("countries_n3", mode="before")
    @classmethod
    def digits_only(cls, val):
        for country in val:
            if not str(country).isdigit():
                raise ValueError("Only numeric codes allowed")

        return val
