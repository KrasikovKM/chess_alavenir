from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from config import *


DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

Base = declarative_base()

engine_sd_api = create_async_engine(DATABASE_URL, pool_pre_ping=True, poolclass=NullPool)
async_session_api = async_sessionmaker(
    engine_sd_api, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    db = async_session_api()
    try:
        yield db
    finally:
        await db.close()


