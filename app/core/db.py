from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings


class DatabaseNotInitializedError(RuntimeError):
    pass

class DatabaseManager:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    def init(self) -> None:
        if self._engine is not None and self._session_factory is not None:
            return

        self._engine = create_async_engine(
            self._settings.postgres_dsn,
            echo=self._settings.postgres_echo,
            pool_size=self._settings.postgres_pool_size,
            max_overflow=self._settings.postgres_max_overflow,
        )

        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            raise DatabaseNotInitializedError(
                "Менеджер базы данных не инициализирован. "
                "Сначала вызовите DatabaseManager.init()."
            )
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        if self._session_factory is None:
            raise DatabaseNotInitializedError(
                "Фабрика сессий не инициализирована. "
                "Сначала вызовите DatabaseManager.init()."
            )
        return self._session_factory

    async def ping(self) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(text("SELECT 1"))
            return result.scalar() == 1

    async def dispose(self) -> None:
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None