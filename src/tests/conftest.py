import pytest
import pytest_asyncio
from typing import AsyncGenerator

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from redis.asyncio import Redis

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
    AsyncEngine
)
from sqlalchemy import text

from api.routers.announcement_router import new_announcement
from api.utils.auth import create_access_token, create_refresh_token
from config import Base, get_test_db_url
from main import app
from api.depends.session_depend import get_session
from api.depends.redis_depend import  get_redis
from db.models.models import UserModel, AnnouncementsModel


@pytest_asyncio.fixture(scope="function")
async def test_async_engine() -> AsyncGenerator[AsyncEngine, None]:
    test_db_url = get_test_db_url()
    engine = create_async_engine(test_db_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("INSERT INTO roles ( role) VALUES ( 'user'), ( 'admin') ON CONFLICT (id) DO NOTHING;"))
        await conn.execute(text("INSERT INTO categories (name) VALUES ('test') ON CONFLICT (id) DO NOTHING;"))
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
def test_session_factory(test_async_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(test_async_engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture(scope="function")
async def db_session(test_session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with test_session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.rollback()
            await session.close()


@pytest_asyncio.fixture(scope="function")
async def redis_client() -> AsyncGenerator[Redis, None]:
    redis = Redis.from_url("redis://localhost:6379", decode_responses=True)
    try:
        await redis.ping()
        yield redis
    except Exception as e:
        pytest.fail(f"Не удалось подключиться к Redis: {e}")
    finally:
        await redis.flushdb()
        await redis.aclose()


@pytest_asyncio.fixture(scope="function")
async def test_user(db_session: AsyncSession) -> UserModel:
    user_yandex_id = 1
    user = UserModel(yandex_id=user_yandex_id, first_name="Test", last_name="User", email="test.user@example.com", is_active=True, role_id=1)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_admin_user(db_session: AsyncSession) -> UserModel:
    admin_yandex_id = 999
    admin_user = UserModel(yandex_id=admin_yandex_id, first_name="Admin", last_name="Test", email="admin.test@example.com", is_active=True, role_id=2)
    db_session.add(admin_user)
    await db_session.commit()
    await db_session.refresh(admin_user)
    return admin_user

@pytest_asyncio.fixture(scope="function")
async def banned_user(db_session: AsyncSession) -> UserModel:
    user_yandex_id = 2
    user = UserModel(yandex_id=user_yandex_id, first_name="Test", last_name="User", email="<EMAIL>", is_active=False, role_id=1)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_announcement(db_session: AsyncSession, test_user: UserModel) -> AnnouncementsModel:
    new_announcement = AnnouncementsModel(
                                          title='test',
                                          description='test',
                                          price=1000,
                                          category_id=1,
                                          user_id=test_user.yandex_id,
                                          geo="test",
                                          type='sale')
    db_session.add(new_announcement)
    await db_session.commit()
    await db_session.refresh(new_announcement)
    return new_announcement



@pytest_asyncio.fixture(scope="function")
async def configured_app(db_session: AsyncSession, redis_client: Redis) -> AsyncGenerator[FastAPI, None]:
    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_redis] = lambda: redis_client
    yield app
    app.dependency_overrides = original_overrides

@pytest_asyncio.fixture(scope="function")
async def async_client(configured_app: FastAPI):
    BASE_URL = "http://test"
    async with AsyncClient(transport=ASGITransport(app=configured_app), base_url=BASE_URL) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def client_with_cookies_user(async_client: AsyncClient, redis_client: Redis, test_user: UserModel):
    user_id = test_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.set(actual_jti, int(test_user.is_active), ex=60)
    await redis_client.set(f"role_{user_id}", 'user', ex=60)
    access_token_data = {'sub': str(user_id)}
    access_token = create_access_token(data=access_token_data)
    async_client.cookies.set("users_refresh_token", refresh_token)
    async_client.cookies.set("users_access_token", access_token)
    return async_client



@pytest_asyncio.fixture(scope="function")
async def client_with_cookies_admin(async_client: AsyncClient, redis_client: Redis, test_admin_user: UserModel):
    user_id = test_admin_user.yandex_id
    refresh_token_data = {'sub': str(user_id), 'type': 'refresh'}
    refresh_token_info = create_refresh_token(refresh_token_data)
    refresh_token = refresh_token_info['token']
    actual_jti = refresh_token_info['token_id']
    await redis_client.set(actual_jti, int(test_admin_user.is_active), ex=60)
    await redis_client.set(f"role_{user_id}", 'admin', ex=60)
    access_token_data = {'sub': str(user_id)}
    access_token = create_access_token(data=access_token_data)
    async_client.cookies.set("users_refresh_token", refresh_token)
    async_client.cookies.set("users_access_token", access_token)
    return async_client