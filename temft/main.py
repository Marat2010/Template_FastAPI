from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from api import router as api_router
from models import db_helper, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    # # === Для случаев без Alembic ===
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)  # Создание таблиц
    #     # await conn.run_sync(Base.metadata.drop_all)  # Удаление таблиц
    yield
    # shutdown
    print(f"=== Закрытие соединений с БД ===")
    await db_helper.dispose()


main_app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
main_app.include_router(api_router, tags=["Item"])


if __name__ == '__main__':
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True)
    # uvicorn.run(main_app, host='127.0.0.1', port=8000)

