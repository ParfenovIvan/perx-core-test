from redis.asyncio import Redis

from app.core.config import Settings


class RedisNotInitializedError(RuntimeError):
    pass


class RedisManager:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client: Redis | None = None

    def init(self) -> None:
        if self._client is not None:
            return

        self._client = Redis.from_url(
            self._settings.redis_dsn,
            decode_responses=self._settings.redis_decode_responses,
        )

    @property
    def client(self) -> Redis:
        if self._client is None:
            raise RedisNotInitializedError(
                "Redis-клиент не инициализирован. "
                "Сначала вызовите RedisManager.init()."
            )
        return self._client

    async def ping(self) -> bool:
        return bool(await self.client.ping())

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None