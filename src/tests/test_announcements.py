import io
import json
from typing import List, Tuple, Any

import pytest
import redis
from fastapi import UploadFile
from httpx import AsyncClient
from redis.asyncio import Redis

from api.utils.auth import create_refresh_token, create_access_token
from db.models.models import UserModel, AnnouncementsModel
from schemas.announcement_schemas import SAnnouncementGet


@pytest.mark.asyncio
async def test_announcement_wo_file(async_client: AsyncClient, test_user: UserModel, redis_client: Redis):
    user_id = test_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.set(actual_jti, int(test_user.is_active), ex=60)
    access_token_data = {'sub': str(user_id)}
    access_token = create_access_token(data=access_token_data)
    form_data = {
        "announcement": json.dumps({
            "title": "Test Announcement",
            "description": "Test description",
            "price": 1000.0,
            "geo": "Test location",
            "status": True,
            "type": "sale",
            "category_id": 1
        })
    }
    async_client.cookies.set("users_refresh_token", refresh_token)
    async_client.cookies.set("users_access_token", access_token)
    response = await async_client.post("/announcements/new-announcement",  data=form_data)
    assert response.status_code == 200
    assert response.json()['ok'] is True
    assert response.json()['detail'] == "Announcement successfully created"


@pytest.mark.asyncio
async def test_announcement_wo_file_failed(async_client: AsyncClient, test_user: UserModel, redis_client: Redis):
    user_id = test_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.set(actual_jti, int(test_user.is_active), ex=60)
    access_token_data = {'sub': str(user_id)}
    access_token = create_access_token(data=access_token_data)
    form_data = {
        "announcement": json.dumps({
            "title": "-",
            "description": "",
            "price": -1000.0,
            "geo": "",
            "status": True,
            "type": "safhle",
            "category_id": -1
        })
    }
    async_client.cookies.set("users_refresh_token", refresh_token)
    async_client.cookies.set("users_access_token", access_token)
    response = await async_client.post("/announcements/new-announcement",  data=form_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_announcement_with_file_success(async_client: AsyncClient, test_user: UserModel, redis_client: Redis):
    user_id = test_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.set(actual_jti, int(test_user.is_active), ex=60)
    access_token_data = {'sub': str(user_id)}
    access_token = create_access_token(data=access_token_data)
    # Create image files
    test_file = io.BytesIO(
        b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00\x01\x00\x01\x00\x00\xFF\xDB\x00C\x00'
        b'\x03\x02\x02\x02\x02\x02\x03\x02\x02\x02\x03\x03\x03\x03\x04\x06\x04\x04\x04\x04\x04'
        b'\x08\x06\x06\x05\x06\t\x08\n\n\t\x08\t\t\n\x0C\x0F\x0C\n\x0B\x0E\x0B\t\t\r\x11\r\x0E'
        b'\x0F\x10\x10\x11\x10\n\x0C\x12\x13\x12\x10\x13\x0F\x10\x10\x10\xFF\xC0\x00\x0B\x08\x00'
        b'\x01\x00\x01\x01\x01\x11\x00\xFF\xC4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x08\xFF\xC4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xDA\x00\x08\x01\x01\x00\x00?\x00\xD2\xCF\xFF\xD9'
    )
    test_file.filename = "test.jpg"
    test_file_content = test_file.read()

    image_file = io.BytesIO(
        b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00\x01\x00\x01\x00\x00\xFF\xDB\x00C\x00'
        b'\x03\x02\x02\x02\x02\x02\x03\x02\x02\x02\x03\x03\x03\x03\x04\x06\x04\x04\x04\x04\x04'
        b'\x08\x06\x06\x05\x06\t\x08\n\n\t\x08\t\t\n\x0C\x0F\x0C\n\x0B\x0E\x0B\t\t\r\x11\r\x0E'
        b'\x0F\x10\x10\x11\x10\n\x0C\x12\x13\x12\x10\x13\x0F\x10\x10\x10\xFF\xC0\x00\x0B\x08\x00'
        b'\x01\x00\x01\x01\x01\x11\x00\xFF\xC4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x08\xFF\xC4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xDA\x00\x08\x01\x01\x00\x00?\x00\xD2\xCF\xFF\xD9'
    )
    image_file.filename = "image.jpg"
    image_file_content = image_file.read()  # read image file

    files = [
        ("file", (image_file.filename, image_file_content, "image/jpeg")),
        ("file", (test_file.filename, test_file_content, "image/jpeg")),
    ]

    form_data = {
        "announcement": json.dumps({
            "title": "Test Announcement",
            "description": "Test description",
            "price": 1000.0,
            "geo": "Test location",
            "status": True,
            "type": "sale",
            "category_id": 1
        })
    }
    async_client.cookies.set("users_refresh_token", refresh_token)
    async_client.cookies.set("users_access_token", access_token)
    response = await async_client.post("/announcements/new-announcement",  data=form_data, files=files)
    assert response.status_code == 200
    assert response.json()['ok'] is True
    assert response.json()['detail'] == "Announcement successfully created"


@pytest.mark.asyncio
async def test_announcement_validation(async_client: AsyncClient, test_user: UserModel, redis_client: Redis):
    user_id = test_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.set(actual_jti, int(test_user.is_active), ex=60)
    access_token_data = {'sub': str(user_id)}
    access_token = create_access_token(data=access_token_data)

    text_file = io.BytesIO(
        b'Test'
    )
    text_file.filename = "test.txt"
    test_file_content = text_file.read()

    image_file = io.BytesIO(
        b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00\x01\x00\x01\x00\x00\xFF\xDB\x00C\x00'
        b'\x03\x02\x02\x02\x02\x02\x03\x02\x02\x02\x03\x03\x03\x03\x04\x06\x04\x04\x04\x04\x04'
        b'\x08\x06\x06\x05\x06\t\x08\n\n\t\x08\t\t\n\x0C\x0F\x0C\n\x0B\x0E\x0B\t\t\r\x11\r\x0E'
        b'\x0F\x10\x10\x11\x10\n\x0C\x12\x13\x12\x10\x13\x0F\x10\x10\x10\xFF\xC0\x00\x0B\x08\x00'
        b'\x01\x00\x01\x01\x01\x11\x00\xFF\xC4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x08\xFF\xC4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xDA\x00\x08\x01\x01\x00\x00?\x00\xD2\xCF\xFF\xD9'
    )
    image_file.filename = "image.jpg"
    image_file_content = image_file.read()  # read image file

    files = [
        ("file", (image_file.filename, image_file_content, "image/jpeg")),
        ("file", (text_file.filename, test_file_content, "plain/txt")),
    ]

    form_data = {
        "announcement": json.dumps({
            "title": "test",
            "description": "test",
            "price": 1000.0,
            "geo": "Test location",
            "status": True,
            "type": "sale",
            "category_id": 1
        }),
    }
    async_client.cookies.set("users_refresh_token", refresh_token)
    async_client.cookies.set("users_access_token", access_token)
    response = await async_client.post("/announcements/new-announcement", data=form_data, files=files)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Incorrect file type'


@pytest.mark.asyncio
async def test_get_announcement(test_user: UserModel, async_client: AsyncClient, test_announcement: AnnouncementsModel):
    response = await async_client.get(f"/announcements/announcement/{test_announcement.id}")
    assert response.status_code == 200
    assert response.json()['id'] == test_announcement.id
    assert response.json()['title'] == test_announcement.title
    assert response.json()['description'] == test_announcement.description
    assert response.json()['price'] == test_announcement.price
    assert response.json()['geo'] == test_announcement.geo
    assert response.json()['status'] == test_announcement.status


@pytest.mark.asyncio
async def test_get_announcement_failed( async_client: AsyncClient):
    response = await async_client.get(f"/announcements/announcement/{34124124}")
    assert response.status_code == 404
    assert response.json()['detail'] == 'Announcement not found'


@pytest.mark.asyncio
async def test_update_announcement(test_user: UserModel,
                                   async_client: AsyncClient,
                                   test_announcement: AnnouncementsModel,
                                   redis_client: Redis):
    user_id = test_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.set(actual_jti, int(test_user.is_active), ex=60)
    access_token_data = {'sub': str(user_id)}
    access_token = create_access_token(data=access_token_data)
    form_data = {
        "announcement": json.dumps({
            "title": "updated",
            "description": "updated"
        })
    }
    async_client.cookies.set("users_refresh_token", refresh_token)
    async_client.cookies.set("users_access_token", access_token)
    response = await async_client.put(f'/announcements/announcement/{test_announcement.id}', data=form_data)
    assert response.status_code == 200
    assert response.json()['ok'] == True
    response = await async_client.get(f'/announcements/announcement/{test_announcement.id}')
    assert response.status_code == 200
    assert response.json()['title'] == 'updated'
    assert response.json()['description'] == 'updated'


@pytest.mark.asyncio
async def test_delete_announcement(test_user: UserModel,
                                   async_client: AsyncClient,
                                   test_announcement: AnnouncementsModel,
                                   redis_client: Redis):
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
    response = await async_client.delete(f'/announcements/announcement/{test_announcement.id}')
    assert response.status_code == 200
    assert response.json()['ok'] == True
    response = await async_client.get(f'/announcements/announcement/{test_announcement.id}')
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_announcements(test_user: UserModel,
                                   async_client: AsyncClient,
                                   test_announcement: AnnouncementsModel):
    response = await async_client.get(f'/announcements/user/{test_user.yandex_id}')
    assert response.status_code == 200
    assert SAnnouncementGet.model_validate(response.json()[0])
    assert response.json()[0]['user_rel']['yandex_id'] == test_user.yandex_id


@pytest.mark.asyncio
async def test_get_feed(test_user: UserModel, test_announcement: AnnouncementsModel, async_client: AsyncClient):
    response = await async_client.get(f'/announcements/feed')
    assert response.status_code == 200
    assert SAnnouncementGet.model_validate(response.json()[0])


