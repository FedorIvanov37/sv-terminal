from pydantic import BaseModel, validator, ValidationError


class User(BaseModel):
    user_id: str

    @validator("user_id")
    def ok(cls, v):
        if v.isdigit:
            raise TypeError("Letters only")

        if '1' in v:
            raise ValueError("a in v")

        return v


try:
    User(user_id="123")
except ValidationError as E:
    print(E.errors())

{'01': '00000239626', '03': '000000010000396', '04': 'Limassol', '05': '3107', '06': '196', '07': 'merch.com', '08': 'PSP'}
{'038': {'01': '00000239626', '03': '000000010000396', '04': 'Limassol', '05': '3107', '06': '196', '07': 'merch.com', '08': 'PSP'}, '033': '5', '027': '30303030433032445531325350334c48474b564c', '028': '00000308254236854496634394423610b892eb6a', '030': '2'}
{'51': 'SOME ONE', '96': '415481%8164', '54': 'HOW ARE YOU', '76': '10000001', '42': '01', '92': '000'}
