import sys

# Проверяем, передан ли аргумент
if len(sys.argv) != 2:
    print("Использование: python mk_file_schemas_ENTITY.py <ENTITY_NAME>")
    sys.exit(1)

ENTITY_NAME = sys.argv[1].capitalize()  # Получаем значение ENTITY_NAME из аргумента командной строки


content = f'''from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel
from pydantic import ConfigDict


class {ENTITY_NAME}Base(BaseModel):
    name: str
    description: str
    is_active: bool
    config: Dict[str, Any] | None = None
    startup_command: str


class {ENTITY_NAME}Create({ENTITY_NAME}Base):
    pass


class {ENTITY_NAME}Update({ENTITY_NAME}Base):
    """Для PUT-запросов (все поля обязательны, как в ItemBase)"""
    pass  # Наследует все поля из {ENTITY_NAME}Base без изменений
    
    
class {ENTITY_NAME}Patch(BaseModel):
    """Схема для PATCH-запросов (все поля опциональны)"""
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    config: Dict[str, Any] | None = None
    startup_command: str | None = None

        
class {ENTITY_NAME}Read({ENTITY_NAME}Base):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
    created_at: datetime
    updated_at: datetime

'''

# Запись в файл
with open(f"schemas/{ENTITY_NAME.lower()}.py", "w") as file:
    file.write(content)

print(f"Файл schemas/{ENTITY_NAME.lower()}.py успешно сделан.")

# ===============================
# import sys

