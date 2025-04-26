from unittest.mock import AsyncMock, patch, MagicMock

import pytest
from httpx import AsyncClient
from redis.asyncio import Redis


from api.utils.auth import create_refresh_token
from db.models.models import UserModel
from authlib.integrations.base_client import OAuthError

from tests.conftest import async_client


@pytest.mark.asyncio
async def test_yandex_login(async_client: AsyncClient):
    response = await async_client.get("/auth/yandex")
    assert response.status_code == 302
    assert "location" in response.headers
    location = response.headers['location']
    assert "oauth.yandex.ru/authorize" in location
    assert "response_type=code" in location


@pytest.mark.asyncio
async def test_yandex_auth_success(async_client: AsyncClient):
    TEST_STATE = "state_for_success_callback_final"
    TEST_CODE = "code_for_success_callback_final"
    EXPECTED_REDIRECT_TARGET = "/docs"

    yandex_user_data = {
        "id": "555666777",
        "first_name": "Яндекс",
        "last_name": "Тест",
        "default_email": "yandex.test.success@example.com",
        "login": "testsuccess"
    }

    mock_authlib_token_response = {
        "access_token": "fake_yandex_at_success",
        "token_type": "bearer",
        "state": TEST_STATE
    }
    APP_ACCESS_TOKEN = "app_access_generated_final"
    APP_REFRESH_TOKEN = "app_refresh_generated_final"
    authlib_auth_path = 'authlib.integrations.starlette_client.StarletteOAuth2App.authorize_access_token'
    authlib_get_path = 'authlib.integrations.starlette_client.StarletteOAuth2App.get'
    register_update_path = 'services.auth_service.AuthService.register_or_update'
    with patch(authlib_auth_path, new_callable=AsyncMock) as mock_authlib_authorize, \
         patch(authlib_get_path, new_callable=AsyncMock) as mock_authlib_get, \
         patch(register_update_path, new_callable=AsyncMock) as mock_register_update:
        mock_authlib_authorize.return_value = mock_authlib_token_response
        mock_user_info_resp_for_patch = MagicMock()
        mock_user_info_resp_for_patch.json.return_value = yandex_user_data
        mock_authlib_get.return_value = mock_user_info_resp_for_patch
        mock_register_update.return_value = {"access_token": APP_ACCESS_TOKEN, "refresh_token": APP_REFRESH_TOKEN}
        response = await async_client.get(
            f"/auth/yandex/auth?code={TEST_CODE}&state={TEST_STATE}",
            follow_redirects=False
        )
        if response.status_code != 303:
            try: error_detail = response.json()
            except Exception: error_detail = response.text
            pytest.fail(f"Expected status 303, got {response.status_code}. Response body: {error_detail}")
        assert response.headers["location"] == EXPECTED_REDIRECT_TARGET
        assert "users_access_token" in response.cookies
        assert response.cookies["users_access_token"] == APP_ACCESS_TOKEN
        assert "users_refresh_token" in response.cookies
        assert response.cookies["users_refresh_token"] == APP_REFRESH_TOKEN
        mock_authlib_authorize.assert_awaited_once()
        mock_authlib_get.assert_awaited_once_with(
            'https://login.yandex.ru/info?format=json',
            token=mock_authlib_token_response
        )
        mock_user_info_resp_for_patch.json.assert_called_once()
        mock_register_update.assert_awaited_once()
        call_args_tuple = mock_register_update.call_args
        assert call_args_tuple is not None, "register_or_update was not called with any arguments"
        positional_args = call_args_tuple.args
        keyword_args = call_args_tuple.kwargs
        passed_user_data = positional_args[0]
        assert isinstance(passed_user_data, dict)
        assert passed_user_data['id'] == yandex_user_data['id']
        assert passed_user_data['default_email'] == yandex_user_data['default_email']
        assert not keyword_args, f"Expected no keyword args for register_or_update, got {keyword_args}"


@pytest.mark.asyncio
async def test_yandex_auth_oauth_error(async_client: AsyncClient):
    TEST_STATE = "invalid_state_v4"
    TEST_CODE = "some_code_v4"
    error_message = "Simulated OAuthError v4."
    authlib_path = 'authlib.integrations.starlette_client.StarletteOAuth2App.authorize_access_token'
    with patch(authlib_path, new_callable=AsyncMock) as mock_authlib_authorize:
        mock_authlib_authorize.side_effect = OAuthError(description=error_message)
        response = await async_client.get(f"/auth/yandex/auth?code={TEST_CODE}&state={TEST_STATE}")
        assert response.status_code == 400
        assert error_message in response.json()["detail"]
        mock_authlib_authorize.assert_awaited_once()


@pytest.mark.asyncio
async def test_yandex_auth_user_banned(async_client: AsyncClient):
    TEST_STATE = "state_for_banned_v4"
    TEST_CODE = "code_for_banned_v4"
    yandex_user_data = {"id": "888999000", "first_name": "Banned", "last_name": "User", "default_email": "banned@example.com"}
    mock_authlib_token_response = {"access_token": "fake_yandex_at_banned", "token_type": "bearer", "state": TEST_STATE}
    authlib_auth_path = 'authlib.integrations.starlette_client.StarletteOAuth2App.authorize_access_token'
    authlib_get_path = 'authlib.integrations.starlette_client.StarletteOAuth2App.get'
    register_update_path = 'services.auth_service.AuthService.register_or_update'
    with patch(authlib_auth_path, new_callable=AsyncMock) as mock_authlib_authorize, \
         patch(authlib_get_path, new_callable=AsyncMock) as mock_authlib_get, \
         patch(register_update_path, new_callable=AsyncMock) as mock_register_update:
        mock_authlib_authorize.return_value = mock_authlib_token_response
        mock_user_info_resp_for_patch = MagicMock()
        mock_user_info_resp_for_patch.json.return_value = yandex_user_data
        mock_authlib_get.return_value = mock_user_info_resp_for_patch
        mock_register_update.return_value = False
        response = await async_client.get(
            f"/auth/yandex/auth?code={TEST_CODE}&state={TEST_STATE}",
            follow_redirects=False
        )
        if response.status_code != 401:
             try: error_detail = response.json()
             except Exception: error_detail = response.text
             pytest.fail(f"Expected status 401, got {response.status_code}. Response body: {error_detail}")
        assert "banned" in response.json()["detail"].lower()
        mock_authlib_authorize.assert_awaited_once()
        mock_authlib_get.assert_awaited_once()
        mock_register_update.assert_awaited_once()

@pytest.mark.asyncio
async def test_refresh_success(async_client: AsyncClient, redis_client: Redis, test_user: UserModel):
    user_id = test_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.set(actual_jti, "1", ex=300)
    cookie_header = f"users_refresh_token={refresh_token}"
    response = await async_client.get( "/auth/refresh", headers={"Cookie": cookie_header})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data.get("ok") is True
    assert "detail" in data
    assert "users_access_token" in response.cookies
    assert response.cookies["users_access_token"] == data["detail"]


@pytest.mark.asyncio
async def test_refresh_failed(async_client: AsyncClient, redis_client: Redis,):
    response = await async_client.get("/auth/refresh")
    assert len(response.cookies) == 0
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_is_banned_in_redis(async_client: AsyncClient, redis_client: Redis, banned_user: UserModel):
    user_id = banned_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.set(actual_jti, int(banned_user.is_active), ex=300)
    cookie_header = f"users_refresh_token={refresh_token}"
    response = await async_client.get("/auth/refresh", headers={"Cookie": cookie_header})
    assert response.json()['detail'] == 'Your account is banned.'
    assert response.status_code == 401
    assert len(response.cookies) == 0

@pytest.mark.asyncio
async def test_refresh_is_banned_in_db(async_client: AsyncClient, redis_client: Redis, banned_user: UserModel):
    user_id = banned_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.delete(actual_jti)
    cookie_header = f"users_refresh_token={refresh_token}"
    response = await async_client.get("/auth/refresh", headers={"Cookie": cookie_header})
    assert response.json()['detail'] == 'Your account is banned.'
    assert response.status_code == 401
    assert len(response.cookies) == 0

@pytest.mark.asyncio
async def test_logout(async_client: AsyncClient, redis_client: Redis, test_user: UserModel):
    user_id = test_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    cookie_header = f"users_refresh_token={refresh_token}"
    response = await async_client.post("/auth/logout", headers={"Cookie": cookie_header})
    assert response.json()['ok']
    assert response.json()['detail'] == 'success logout'
    assert response.status_code == 200
    assert len(response.cookies) == 0

