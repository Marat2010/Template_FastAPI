import sys

# Проверяем, передан ли аргумент
if len(sys.argv) != 2:
    print("Использование: python mk_file_api_api_v1___init.py <ENTITY_NAME>")
    sys.exit(1)

ENTITY_NAME = sys.argv[1].capitalize()  # Получаем значение ENTITY_NAME из аргумента командной строки
ENTITY_NAME_low = ENTITY_NAME.lower()

content = f'''from fastapi import APIRouter
from core.config import settings

from .{ENTITY_NAME_low} import router as {ENTITY_NAME_low}_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    {ENTITY_NAME_low}_router,
    prefix=settings.api.v1.{ENTITY_NAME_low},
    # prefix=settings.api.v1.item2,
)

'''

# Запись в файл
with open(f"api/api_v1/__init__.py", "w") as file:
    file.write(content)

print(f"Файл api/api_v1/__init__.py успешно сделан.")

