import datetime
import os

import aiofiles
from fastapi import UploadFile

from db.repositories.announcemets_repository import AnnouncementRepository
from schemas.announcement_schemas import SAnnouncement


class AnnouncementService:
    def __init__(self, repository: AnnouncementRepository):
        self.repository = repository


    async def new_announcement(self, announcement: SAnnouncement, user_id: int):
        announcement_dict = announcement.model_dump()
        await self.repository.create(announcement_dict, user_id)
        return True


    async def get_announcement(self, announcement_id: int):
        result = await self.repository.get_by_id(announcement_id)
        if result is None:
            return None
        return result


    async def update_announcement(self, announcement_id: int,
                                  announcement: SAnnouncement,
                                  user_id: int):
        announcement_dict = announcement.model_dump()
        await self.repository.update(announcement_id, user_id, announcement_dict)
        return True
