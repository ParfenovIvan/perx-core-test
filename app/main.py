from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.lifespan import lifespan

app = FastAPI(
    title="Perx Test",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)