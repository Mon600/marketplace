
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.models import UserModel, CategoriesModel


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, name: str):
        new_category = CategoriesModel(name=name)
        self.session.add(new_category)
        await self.session.commit()
        return True

    async def get_all(self):
        query = select(CategoriesModel)
        categories = await self.session.execute(query)
        result = categories.scalars().all()
        return result

    async def delete(self, id: int):
        query = delete(CategoriesModel).where(CategoriesModel.id == id)
        await self.session.execute(query)
        await self.session.commit()
        return True


    async def update(self, data: dict):
        query = update(CategoriesModel).where(CategoriesModel.id == data['id']).values(name = data['name'])
        await self.session.execute(query)
        await self.session.commit()
        return True