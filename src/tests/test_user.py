import pytest
from httpx import AsyncClient
from redis.asyncio import Redis

from api.utils.auth import create_refresh_token, create_access_token
from db.models.models import UserModel
from schemas.user_schemas import SUser


@pytest.mark.asyncio
async def test_user_get_info(async_client: AsyncClient, redis_client: Redis, test_user: UserModel):
    user_id = test_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.set(actual_jti, int(test_user.is_active), ex=60)
    access_token_data = {'sub': str(user_id)}
    access_token = create_access_token(data=access_token_data)
    async_client.cookies.set("users_refresh_token", refresh_token)
    async_client.cookies.set("users_access_token", access_token)
    response = await async_client.get(f'/users/')
    assert response.status_code == 200
    assert response.json()['yandex_id'] == test_user.yandex_id
    assert SUser.model_validate(response.json())

@pytest.mark.asyncio
async def test_user_get_info_by_id(async_client: AsyncClient, redis_client: Redis, test_user: UserModel):
    response = await async_client.get(f'/users/{test_user.yandex_id}')
    assert response.status_code == 200
    assert response.json()['yandex_id'] == test_user.yandex_id


@pytest.mark.asyncio
async def test_update_user(async_client: AsyncClient, redis_client: Redis, test_user: UserModel):
    user_id = test_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.set(actual_jti, int(test_user.is_active), ex=60)
    access_token_data = {'sub': str(user_id)}
    access_token = create_access_token(data=access_token_data)
    async_client.cookies.set("users_refresh_token", refresh_token)
    async_client.cookies.set("users_access_token", access_token)
    new_data = {'first_name': 'updated',
                'last_name': 'updated',
                'phone': '88005553535',}
    response = await async_client.put(f'/users/update/', json=new_data)
    assert response.status_code == 200
    response = await async_client.get(f'/users/')
    assert response.status_code == 200
    assert response.json()['yandex_id'] == test_user.yandex_id
    assert response.json()['first_name'] == 'updated'
    assert response.json()['last_name'] == 'updated'