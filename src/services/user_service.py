from db.repositories.user_repository import UserRepository
from schemas.user_schemas import SUser, SChange



class UserService:
    def __init__(self, repository: UserRepository):
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


    async def get_user_info(self, user_id: str):
        user = await self.repository.get_user_by_id(int(user_id))
        if not user:
            return None
        else:
            result = SUser.model_validate(user)
            return result

    async def update_user_info(self, user_id: str, new_data: SChange):
        data = new_data.model_dump()
        cleaned_data = await self.clean_dict(data)
        if result := await self.repository.update(int(user_id), cleaned_data):
            return result
        else:
            return None

    async def get_user_role(self, user_id: int):
        user = await self.repository.check_rights(user_id)
        return user

    async def ban(self, user_id):
        result = await self.repository.ban_user()