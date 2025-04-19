from redis.asyncio import Redis

from db.repositories.user_repository import UserRepository


class AdminService:
    def __init__(self,
                 u_repository: UserRepository,
                 redis: Redis):
        self.repository = u_repository
        self.redis = redis

    async def ban(self, user_id: int):
        tokens = await self.repository.ban(user_id)
        for token in tokens:
            await self.redis.set(token, int(False), ex=900)
        return True