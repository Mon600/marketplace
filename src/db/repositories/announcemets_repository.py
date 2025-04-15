from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, lazyload, selectinload

from db.models.models import AnnouncementsModel

class AnnouncementRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, announcement: dict, user_id: int):
        new_announcement = AnnouncementsModel(**announcement, user_id = user_id)
        self.session.add(new_announcement)
        await self.session.commit()
        return new_announcement.id


    async def get_by_id(self, announcement_id: int):
        query = (select(AnnouncementsModel)
                .where(AnnouncementsModel.id == announcement_id)
                .options(
                         joinedload(AnnouncementsModel.user_rel),
                                 selectinload(AnnouncementsModel.file_rel),
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

    async def delete(self, announcement_id: int, user_id: int) -> None:
        query = (delete(AnnouncementsModel)
                 .where(AnnouncementsModel.id == announcement_id,
                        AnnouncementsModel.user_id == user_id)
                 )
        await self.session.execute(query)
        await self.session.commit()



