from typing import Optional, List

from schemas.announcement_schemas import SAnnouncementGet
from schemas.user_schemas import SUser


class SUserByID(SUser):
    announcements_rel: Optional[List[SAnnouncementGet]]