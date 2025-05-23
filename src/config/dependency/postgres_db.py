# -*- coding: utf-8 -*-


from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from src.config.settings import Settings
from src.utils.common import Singleton


class DatabasePostgres(metaclass=Singleton):
    def __init__(self) -> None:
        self._engine: AsyncEngine = self._create_engine()  # type: ignore[assignment]
        self._session_maker: async_sessionmaker[AsyncSession] = (
            self._create_session_factory()
        )

    async def ping(self) -> None:
        async with self.session as session:
            await session.execute(text("SELECT 1;"))
            print("Database connection is alive.")

    @property
    def session(self) -> AsyncSession:
        return self._session_maker()  # type: ignore[no-any-return,operator, unused-ignore] # noqa

    def _create_engine(self) -> async_sessionmaker[AsyncSession]:  # noqa: PLR6301
        return create_async_engine(Settings().DATABASE_POSTGRES_URL)  # type: ignore[return-value, call-arg]

    def _create_session_factory(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def close(self) -> None:
        await self._engine.dispose()
