import json

from redis.asyncio import Redis

from db.repositories.user_repository import UserRepository
from schemas.dificult_user_schema import SUserByID
from schemas.user_schemas import SUser, SChange


class UserService:
    def __init__(self, repository: UserRepository, redis: Redis):
        self.repository = repository
        self.redis = redis

    @staticmethod
    async def clean_dict(data: dict) -> dict:
        null_keys = set()
        for i in data:
            if not data[i]:
                null_keys.add(i)
        for i in null_keys:
            del data[i]
        return data


    async def get_user_info(self, user_id: str) -> SUserByID | None:
        user_cache = await self.redis.get(user_id)
        if user_cache:
            return json.loads(user_cache)
        user = await self.repository.get_user_by_id(int(user_id))
        if not user:
            return None
        else:
            result = SUserByID.model_validate(user)
            await self.redis.set(user_id, json.dumps(result.model_dump()), ex=86400)
            return user

    async def update_user_info(self, user_id: str, new_data: SChange):
        data = new_data.model_dump()
        cleaned_data = await self.clean_dict(data)
        if result := await self.repository.update(int(user_id), cleaned_data):
            await self.redis.delete(user_id)
            return result
        else:
            return None

    async def get_user_role(self, user_id: int):
        user = await self.repository.check_rights(user_id)
        return user
