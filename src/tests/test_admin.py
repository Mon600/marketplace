import pytest
from httpx import AsyncClient

from api.utils.auth import create_access_token, create_refresh_token
from db.models.models import UserModel, AnnouncementsModel, RoleModel


@pytest.mark.asyncio
async def test_ban_user(client_with_cookies_admin: AsyncClient):
    response = await client_with_cookies_admin.put('/admin/ban/1')
    assert response.status_code == 200
    assert response.json()['ok'] == True

@pytest.mark.asyncio
async def test_ban_user_failed(client_with_cookies_user: AsyncClient):
    response = await client_with_cookies_user.put('/admin/ban/1')
    assert response.status_code == 403
    assert response.json()['detail'] == "Access denied"


@pytest.mark.asyncio
async def test_unban_user(client_with_cookies_admin: AsyncClient):
    response = await client_with_cookies_admin.put('/admin/unban/1')
    assert response.status_code == 200
    assert response.json()['ok'] == True

@pytest.mark.asyncio
async def test_unban_user_failed(client_with_cookies_user: AsyncClient):
    response = await client_with_cookies_user.put('/admin/unban/1')
    assert response.status_code == 403
    assert response.json()['detail'] == "Access denied"


@pytest.mark.asyncio
async def test_deactivate_announcement(client_with_cookies_admin: AsyncClient, test_announcement: AnnouncementsModel):
    response = await client_with_cookies_admin.put(f'/admin/deactivate/{test_announcement.id}/')
    assert response.status_code == 200
    assert response.json()['ok'] == True


@pytest.mark.asyncio
async def test_deactivate_announcement_failed(client_with_cookies_user: AsyncClient, test_announcement: AnnouncementsModel):
    response = await client_with_cookies_user.put(f'/admin/deactivate/{test_announcement.id}/')
    assert response.status_code == 403
    assert response.json()['detail'] == "Access denied"

@pytest.mark.asyncio
async def test_give_role(client_with_cookies_admin: AsyncClient, test_user: UserModel):
    response = await client_with_cookies_admin.put(f'/admin/give-role/{test_user.yandex_id}/2')
    assert response.status_code == 200
    assert response.json()['ok'] == True

@pytest.mark.asyncio
async def test_give_role_failed(client_with_cookies_user: AsyncClient, test_user: UserModel):
    response = await client_with_cookies_user.put(f'/admin/give-role/{test_user.yandex_id}/2')
    assert response.status_code == 403
    assert response.json()['detail'] == "Access denied"



