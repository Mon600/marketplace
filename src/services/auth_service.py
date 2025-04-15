from authlib.integrations.starlette_client import OAuth
from config import get_yandex_secrets
from api.utils.auth import create_token
from db.repositories.user_repository import UserRepository
from schemas.user_schemas import SRegister


class AuthService:
    def __init__(self, repository: UserRepository):
        self.secrets = get_yandex_secrets()
        self.repository = repository
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
        id = await self.repository.create_or_update(user_data)
        access_token = create_token({'sub': f'{id}'})
        refresh_token = create_token({'sub': f'{id}'}, expire_days=30)
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def refresh(self, user_id: int):
        access_token = create_token({'sub': f'{user_id}'})
        return access_token