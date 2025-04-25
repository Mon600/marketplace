from redis.asyncio import Redis

from db.repositories.admin_repository import AdminRepository


class AdminService:
    def __init__(self,
                 repository: AdminRepository,
                 redis: Redis):
        self.repository = repository
        self.redis = redis

    async def ban(self, user_id: int):
        tokens = await self.repository.ban(user_id)
        for token in tokens:
            await self.redis.set(token, int(False), keepttl=True)
        return True

    async def unban(self, user_id: int):
        tokens = await self.repository.unban(user_id)
        for token in tokens:
            await self.redis.set(token, int(True), keepttl=True)
        return True

    async def delete_announcement(self, announcement_id: int) -> bool:
        await self.repository.delete_announcement(announcement_id)
        return True

    async def give_role(self, user_id: int, role_id: int):
        await self.repository.give_role(user_id, role_id)
        await self.redis.delete(f'role_{user_id}')
        return True

