from db.repositories.announcemets_repository import AnnouncementRepository
from schemas.announcement_schemas import SAnnouncement, SAnnouncementGet


class AnnouncementService:
    def __init__(self, repository: AnnouncementRepository):
        self.repository = repository

    @staticmethod
    async def clean_dict(data: dict) -> dict:
        null_keys = set()
        for i in data:
            if not data[i]:
                null_keys.add(i)
        for i in null_keys:
            del data[i]
        return data


    async def new_announcement(self, announcement: SAnnouncement, user_id: int):
        announcement_dict = announcement.model_dump()
        id = await self.repository.create(announcement_dict, user_id)
        return id


    async def get_announcement(self, announcement_id: int) -> SAnnouncementGet | None:
        result = await self.repository.get_by_id(announcement_id)
        if result is None:
            return None
        return result


    async def update_announcement(self, announcement_id: int,
                                  announcement: SAnnouncement,
                                  user_id: int) -> bool:
        announcement_dict = announcement.model_dump()
        announcement_dict = await self.clean_dict(announcement_dict)
        await self.repository.update(announcement_id, user_id, announcement_dict)
        return True

    async def delete_announcement(self, announcement_id: int, user_id: int) -> bool:
        await self.repository.delete(announcement_id, user_id)
        return True
