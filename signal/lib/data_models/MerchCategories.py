from pydantic import BaseModel, Field, field_validator


class MerchantCategoryCode(BaseModel):
    code: str = Field(..., min_length=4, max_length=4)
    description: str = Field(..., min_length=0, max_length=1024)

    @field_validator("code", mode="before")
    @classmethod
    def validate_mcc(cls, val):
        val = str(val).zfill(4)

        if not val.isdigit():
            raise ValueError("MCC should contain digits only")

        return val


class MerchantCategoryCodes(BaseModel):
    merchant_category_codes: list[MerchantCategoryCode] = list()
