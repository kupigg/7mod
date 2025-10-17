from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session

from core.settings import settings


DATABASE_URL = settings.postgres.url


engine = create_async_engine(DATABASE_URL, echo=True)
sync_engine = create_engine(settings.postgres.url_sync, echo=True)
Base = declarative_base()


async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


def get_sync_db_session() -> Session:
    with Session(sync_engine) as session:
        yield session


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
