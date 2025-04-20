from authlib.integrations.starlette_client import OAuth
from config import get_yandex_secrets
from api.utils.auth import create_refresh_token, create_access_token
from db.repositories import token_repository
from db.repositories.token_repository import TokenRepository
from db.repositories.user_repository import UserRepository
from schemas.user_schemas import SRegister
from redis.asyncio import Redis


class AuthService:
    def __init__(self, user_repository: UserRepository, token_repository: TokenRepository, redis: Redis):
        self.secrets = get_yandex_secrets()
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.redis = redis
        self.oauth = OAuth()
        self.oauth.register(
            name='yandex',
            client_id=self.secrets['client_id'],
            client_secret=self.secrets['client_secret'],
            authorize_url='https://oauth.yandex.ru/authorize',
            access_token_url='https://oauth.yandex.ru/token',
            userinfo_endpoint='https://login.yandex.ru/info',
            client_kwargs={
                'scope': 'login:email login:info',
                'response_type': 'code',
            },
        )


    async def register_or_update(self, user):
        user_data = SRegister(
            yandex_id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['default_email'],
        ).model_dump()
        user = await self.user_repository.create_or_update(user_data)
        id = int(user[0])
        is_active = user[1]
        if is_active:
            access_token = create_access_token({'sub': f'{id}'})
            refresh_token_info = create_refresh_token({'sub': f'{id}'})
            token_id = refresh_token_info['token_id']
            refresh_token = refresh_token_info['token']
            await self.token_repository.add_token(id, token_id)
            await self.redis.set(token_id, int(is_active), ex=86400 * 30)
            return {"access_token": access_token, "refresh_token": refresh_token}
        return False

    @staticmethod
    async def refresh(user_id: int):
        access_token = create_access_token({'sub': f'{user_id}'})
        return access_token

    async def logout(self, token_id: str):
        await self.token_repository.delete(token_id)
        await self.redis.delete(token_id)
        return True