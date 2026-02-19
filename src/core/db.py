from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from models.base_model import Base
from core.settings import settings


class DataBase:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url)
        self._async_session_maker = async_sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator:
        async with self._async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()


db_instance = DataBase(settings.DATA_BASE_URL_asyncpg)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_instance.session() as session:
        yield session
