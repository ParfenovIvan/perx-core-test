from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.db import DatabaseManager
from app.core.redis import RedisManager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()

    db_manager = DatabaseManager(settings)
    db_manager.init()
    await db_manager.ping()

    redis_manager = RedisManager(settings)
    redis_manager.init()
    await redis_manager.ping()

    app.state.settings = settings
    app.state.db = db_manager
    app.state.redis = redis_manager

    try:
        yield
    finally:
        await redis_manager.close()
        await db_manager.dispose()