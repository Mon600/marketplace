from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.models import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_or_update(self, user):
        query = (
            insert(UserModel)
            .values(**user)
            .on_conflict_do_update(
                index_elements=["yandex_id"],
                set_=user
            )
            .returning(UserModel.yandex_id)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalars().one()

    async def get_user_by_id(self, id: int):
        query = select(UserModel).where(UserModel.yandex_id == id)
        user = await self.session.execute(query)
        return user.scalars().one_or_none()

    async def update(self, user_id: int, data: dict):
        print(data)
        query = update(UserModel).where(UserModel.yandex_id == user_id).values(**data)
        await self.session.execute(query)
        await self.session.commit()
        return True