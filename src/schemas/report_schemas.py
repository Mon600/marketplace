from typing import Optional

from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.sql.annotation import Annotated


class SReport(BaseModel):
    announcement_id: int
    reason: Optional[str] = ''
    type: str = 'spam'

report_schema = Annotated[SReport, Depends()]

class SReportExtended(SReport):
    user_id: int


