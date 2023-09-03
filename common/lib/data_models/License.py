from pydantic import BaseModel
from datetime import datetime


class LicenseInfo(BaseModel):
    accepted: bool = False
    last_acceptance_date: datetime | None = None
    show_agreement: bool = True
