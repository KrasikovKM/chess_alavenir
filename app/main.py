import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers import main_router
from database.connection import engine_sd_api, Base
import database.models  # Импортируем, чтобы модели зарегистрировались в Base.metadata

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем таблицы при запуске
    async with engine_sd_api.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    root_path="/chess_service"
)


app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=True
    )
