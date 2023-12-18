from pydantic import BaseModel, field_validator
from common.lib.data_models.Countries import Countries
from common.lib.data_models.Currencies import Currencies


class Dictionaries(BaseModel):
    currencies: Currencies | None = Currencies()
    countries: Countries | None = Countries()

    @field_validator("currencies", mode="before")
    @classmethod
    def substitute_none_currencies(cls, val):
        if val is None:
            return Currencies()

        return val

    @field_validator("countries", mode="before")
    @classmethod
    def substitute_none_countries(cls, val):
        if val is None:
            return Countries()

        return val
