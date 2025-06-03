from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from url_alias.infrastructure.config.db import DatabaseConfig


async def get_engine(config: DatabaseConfig) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(
        config.uri,
        echo=config.ECHO,
        echo_pool=config.ECHO_POOL,
        pool_size=config.POOL_SIZE,
        max_overflow=config.MAX_OVERFLOW,
    )
    yield engine
    await engine.dispose()


async def get_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


async def get_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
