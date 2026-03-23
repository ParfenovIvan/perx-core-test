from collections.abc import AsyncIterator

from fastapi import Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.db import DatabaseManager
from app.core.redis import RedisManager


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_db_manager(request: Request) -> DatabaseManager:
    return request.app.state.db


def get_redis_manager(request: Request) -> RedisManager:
    return request.app.state.redis


async def get_db_session(
    request: Request,
) -> AsyncIterator[AsyncSession]:
    db_manager = get_db_manager(request)

    async with db_manager.session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


def get_redis(request: Request) -> Redis:
    redis_manager = get_redis_manager(request)
    return redis_manager.client