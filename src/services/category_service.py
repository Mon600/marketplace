import json

from cryptography.hazmat.primitives.serialization.pkcs7 import serialize_certificates
from redis.asyncio import Redis
from unicodedata import category

from db.repositories.category_repository import CategoryRepository
from schemas.category_schemas import SCategory


class CategoryService:
    def __init__(self, repository: CategoryRepository, redis: Redis):
        self.repository = repository
        self.redis = redis

    async def create_category(self, name: str):
        res = await self.repository.create(name.title())
        await self.redis.delete("all_categories")
        return res

    async def get_categories(self):
        if category_cache := await self.redis.get('all_categories'):
            raise json.loads(category_cache)
        res = await self.repository.get_all()
        serialize_categories = []
        for category in res:
            serialize_categories.append(SCategory.model_validate(category).model_dump())
        await self.redis.set('all_categories', json.dumps(serialize_categories), ex=3600)
        return res

    async def delete_category(self, id: int):
        res = await self.repository.delete(id)
        await self.redis.delete("all_categories")
        return res

    async def update_category(self, data: SCategory):
        data_dict = data.model_dump()
        data_dict['name'] = data_dict['name'].title()
        res = await self.repository.update(data_dict)
        await self.redis.delete("all_categories")
        return res