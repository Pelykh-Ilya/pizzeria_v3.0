from dataclasses import dataclass
from typing import Type

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker

from pizzeria_app.app.dto.config import PostgresConfig


@dataclass
class Postgres:
    engine: AsyncEngine
    session: Type[AsyncSession]


def create_database(config: PostgresConfig) -> Postgres:
    engine: AsyncEngine = create_async_engine(
        config.dsn,
        pool_pre_ping=True,
        echo=config.echo,
        pool_size=config.pool_size,
        max_overflow=config.pool_max_overflow,
    )
    async_session: Type[AsyncSession] = async_sessionmaker(  # type: ignore
        engine,
        expire_on_commit=False
    )
    return Postgres(engine=engine, session=async_session)
