import sys

# Проверяем, передан ли аргумент
if len(sys.argv) != 2:
    print("Использование: python mk_file_models___init.py <ENTITY_NAME>")
    sys.exit(1)

ENTITY_NAME = sys.argv[1]  # Получаем значение ENTITY_NAME из аргумента командной строки

content = f"""__all__ = (
    "db_helper",
    "Base",
    "{ENTITY_NAME.capitalize()}",
)
from .db_helper import db_helper
from .base import Base
from .{ENTITY_NAME} import {ENTITY_NAME.capitalize()}

"""

# Запись в файл
with open(f"models/__init__.py", "w") as file:
    file.write(content)

print(f"Файл models/__init__.py успешно создан.")
