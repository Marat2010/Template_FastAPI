from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from core.logger import logger
from api import router as api_router
from core.middleware.http_logging import LoggingMiddleware
from models import db_helper
from utils.db import wait_for_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logger.info("Starting application...")
    logger.debug(f"Using settings: {settings.model_dump_json(indent=2)}")

    try:
        # Проверка подключения к БД
        await wait_for_db(db_helper.engine)
        # # === Для случаев без Alembic ===
        # async with db_helper.engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.create_all)  # Создание таблиц
        #     # await conn.run_sync(Base.metadata.drop_all)  # Удаление таблиц
        logger.info("Database connection established")

    except Exception as e:
        logger.critical(f"Failed to initialize application: {str(e)}")
        raise

    yield
    # shutdown
    logger.info("Shutting down application...")
    try:
        await db_helper.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    title=settings.api.title,
    version=settings.api.version,
    # docs_url=f"{settings.api.prefix}/docs",
    # redoc_url=f"{settings.api.prefix}/redoc"
)
app.include_router(api_router, tags=["Item"])


# Добавьте middleware к приложению
app.add_middleware(LoggingMiddleware)

if __name__ == '__main__':
    logger.info(f"Starting server on {settings.run.host}:{settings.run.port}")
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        log_config=None,  # Отключаем стандартное логирование uvicorn
        access_log=False  # Отключаем access-логи (они будут через middleware)
    )
    # uvicorn.run(main_app, host='0.0.0.0', port=8000)

