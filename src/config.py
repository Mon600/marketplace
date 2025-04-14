import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

def get_db_url():
    return os.getenv("DB_URL")


def get_auth_data():
    return {"secret_key": os.getenv("SECRET_KEY"), "algorithm":os.getenv("ALGORITHM")}

def get_yandex_secrets():
    return {"client_id": os.getenv("YANDEX_CLIENT_ID"), "client_secret": os.getenv("YANDEX_CLIENT_SECRET")}


engine = create_async_engine(
    url=get_db_url()
)


async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass