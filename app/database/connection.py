from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from config import *


DATABASE_URL = f'mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class Base(DeclarativeBase):
    pass

engine_sd_api = create_async_engine(DATABASE_URL, pool_pre_ping=True, poolclass=NullPool)
async_session_api = async_sessionmaker(
    engine_sd_api, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    async with async_session_api() as db:
        yield db


