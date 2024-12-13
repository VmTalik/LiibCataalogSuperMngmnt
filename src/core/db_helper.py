from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from core.config import settings, get_db_url
from typing import AsyncGenerator


class DatabaseHelper:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            max_overflow: int = 10,
            pool_size: int = 5
    ) -> None:
        self.url = url
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


def create_db_helper(
        test_db: bool = False,
        echo: bool = settings.engine_config.echo,
        echo_pool: bool = settings.engine_config.echo_pool,
        max_overflow: int = settings.engine_config.max_overflow,
        pool_size: int = settings.engine_config.pool_size
) -> DatabaseHelper:
    return DatabaseHelper(
        url=get_db_url(test_db=test_db),
        echo=echo,
        echo_pool=echo_pool,
        max_overflow=max_overflow,
        pool_size=pool_size
    )


db_helper = create_db_helper()
