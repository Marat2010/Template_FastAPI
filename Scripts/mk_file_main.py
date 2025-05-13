import sys

# Проверяем, передан ли аргумент
if len(sys.argv) != 2:
    print("Использование: python mk_file_main.py <ENTITY_NAME>")
    sys.exit(1)

ENTITY_NAME = sys.argv[1].capitalize()  # Получаем значение ENTITY_NAME из аргумента командной строки
ENTITY_NAME_low = ENTITY_NAME.lower()

content = f'''from contextlib import asynccontextmanager

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
main_app.include_router(api_router, tags=["{ENTITY_NAME}"])


if __name__ == '__main__':
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True)
    # uvicorn.run(main_app, host='0.0.0.0', port=8000)

'''

# Запись в файл
with open(f"main.py", "w") as file:
    file.write(content)

print(f"Файл main.py успешно сделан.")

