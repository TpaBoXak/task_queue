from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager


from .base import Base
from .task import (
    Task,
    TaskStatus
)


class DataBaseHelper:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10,
    ):
        self.engine = create_async_engine(
                url=url,
                echo=echo,
                echo_pool=echo_pool,
                pool_size=pool_size,
                max_overflow=max_overflow,
        )

        self.session_factory: async_sessionmaker[AsyncSession] = \
                async_sessionmaker(
                        bind=self.engine,
                        autoflush=False,
                        autocommit=False,
                        expire_on_commit=False,
                )
    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self):
        async with self.session_factory() as session:
            yield session

    @asynccontextmanager
    async def session_getter_context(self):
        async with self.session_factory() as session:
            yield session
        
