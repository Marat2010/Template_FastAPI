import sys

# Проверяем, передан ли аргумент
if len(sys.argv) != 2:
    print("Использование: python mk_file_models_ENTITY.py <ENTITY_NAME>")
    sys.exit(1)

ENTITY_NAME = sys.argv[1]  # Получаем значение ENTITY_NAME из аргумента командной строки

content = f"""from datetime import datetime
from sqlalchemy import JSON, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

class {ENTITY_NAME.capitalize()}(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column()
    config: Mapped[JSON] = mapped_column(type_=JSON, nullable=True)
    startup_command: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

"""

# Запись в файл
with open(f"models/{ENTITY_NAME}.py", "w") as file:
    file.write(content)

print(f"Файл models/{ENTITY_NAME}.py успешно создан.")

