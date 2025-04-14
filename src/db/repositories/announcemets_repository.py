from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models.models import AnnouncementsModel

class AnnouncementRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, announcement: dict, user_id: int):
        new_announcement = AnnouncementsModel(**announcement, user_id = user_id)
        self.session.add(new_announcement)
        await self.session.commit()
        return new_announcement.id

    async def get_announcement_user_by_id(self, announcement_id: int):
        query = select(AnnouncementsModel.user_id).where(AnnouncementsModel.id == announcement_id)
        user_id = await self.session.execute(query)
        return user_id.scalars().one_or_none()

    async def get_by_id(self, announcement_id: int):
        query = (select(AnnouncementsModel)
                .where(AnnouncementsModel.id == announcement_id)
                .options(
                         joinedload(AnnouncementsModel.user_rel)
                        )
                )
        announcement = await self.session.execute(query)
        result = announcement.scalars().one_or_none()
        return result

    async def update(self, announcement_id: int, user_id: int, announcement: dict):
        query = (update(AnnouncementsModel)
                 .where(
            AnnouncementsModel.id == announcement_id,
            AnnouncementsModel.user_id == user_id)
            .values(**announcement)
        )
        await self.session.execute(query)
        await self.session.commit()
        return True

    async def update_files(self, dirs: dict, announcement_id: int, user_id: int):
        query = update(AnnouncementsModel).where(AnnouncementsModel.id == announcement_id,
                                        AnnouncementsModel.user_id == user_id).values(**dirs)
        await self.session.execute(query)
        await self.session.commit()
        return True

    async def delete_files(self, announcement_id: int, user_id: int, files: dict):
        query = (update(AnnouncementsModel)
                 .where(AnnouncementsModel.id == announcement_id, AnnouncementsModel.user_id == user_id)
                 .values(**files))
        await self.session.execute(query)
        await self.session.commit()
        return True

