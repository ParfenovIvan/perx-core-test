from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_session, get_redis

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/db")
async def health_db(
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    result = await session.execute(text("SELECT 1"))
    db_status = "ok" if result.scalar() == 1 else "error"
    return {"database": db_status}


@router.get("/redis")
async def health_redis(
    redis: Redis = Depends(get_redis),
) -> dict[str, str]:
    redis_status = "ok" if await redis.ping() else "error"
    return {"redis": redis_status}