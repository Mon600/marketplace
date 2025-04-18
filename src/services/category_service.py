from db.repositories.category_repository import CategoryRepository
from schemas.category_schemas import SCategory


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository


    async def create_category(self, name: str):
        res = await self.repository.create(name.title())
        return res

    async def get_categories(self):
        res = await self.repository.get_all()
        return res

    async def delete_category(self, id: int):
        res = await self.repository.delete(id)
        return res

    async def update_category(self, data: SCategory):
        data_dict = data.model_dump()
        data_dict['name'] = data_dict['name'].title()
        res = await self.repository.update(data_dict)
        return res