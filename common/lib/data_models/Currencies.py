from pydantic import BaseModel, field_validator


class Currencies(BaseModel):
    currencies_a3: list[str] = list()
    currencies_n3: list[str] = list()

    @field_validator("currencies_a3", mode="before")
    @classmethod
    def non_digits_only(cls, val):
        for currency in val:
            if not str(currency).isalpha():
                raise ValueError("Only alphabetic allowed")

        return val

    @field_validator("currencies_n3", mode="before")
    @classmethod
    def digits_only(cls, val):
        for currency in val:
            if not str(currency).isdigit():
                raise ValueError("Only numeric codes allowed")

        return val
