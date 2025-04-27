import pytest
from httpx import AsyncClient
from redis.asyncio import Redis

from api.utils.auth import create_refresh_token, create_access_token
from db.models.models import UserModel
from tests.conftest import test_admin_user


@pytest.mark.asyncio
async def test_get_category(async_client: AsyncClient):
    response = await async_client.get('/category/')
    assert response.status_code == 200
    assert response.json()


@pytest.mark.asyncio
async def test_create_category(client_with_cookies_admin: AsyncClient):
    new_category = {
        'name': "test_23232"
    }
    response = await client_with_cookies_admin.post('/category/', params=new_category)
    assert response.status_code == 200
    assert response.json()['ok'] == True
    response = await client_with_cookies_admin.get('/category/')
    assert response.json()[-1]['name'] == 'Test_23232'

@pytest.mark.asyncio
async def test_create_category_failed(client_with_cookies_user: AsyncClient):
    new_category = {
        'name': "test_23232"
    }
    response = await client_with_cookies_user.post('/category/', params=new_category)
    assert response.status_code == 403
    assert response.json()['detail'] == "Access denied"


@pytest.mark.asyncio
async def test_delete_category(client_with_cookies_admin: AsyncClient):
    response = await client_with_cookies_admin.delete(f'/category/{1}')
    assert response.status_code == 200
    assert response.json()['ok'] == True
    response = await client_with_cookies_admin.get('/category/')
    assert not response.json()


@pytest.mark.asyncio
async def test_update_category(client_with_cookies_admin: AsyncClient):
    new_category = {
        'name': "test_23232"
    }
    response = await client_with_cookies_admin.put('/category/1', params=new_category)
    assert response.status_code == 200
    response = await client_with_cookies_admin.get('/category/')
    assert response.json()[0]['name'] == 'Test_23232'


@pytest.mark.asyncio
async def test_update_category_failed(client_with_cookies_user: AsyncClient):
    new_category = {
        'name': "test_23232"
    }
    response = await client_with_cookies_user.put('/category/1', params=new_category)
    assert response.status_code == 403
    assert response.json()['detail'] == "Access denied"


