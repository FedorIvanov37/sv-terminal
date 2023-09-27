from pydantic import BaseModel
from datetime import datetime
from uuid import uuid1


class LicenseInfo(BaseModel):
    accepted: bool = False
    last_acceptance_date: datetime | None = None
    show_agreement: bool = True
    license_id: str = str(uuid1())
