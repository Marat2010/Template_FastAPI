content = f"""from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from core.config import settings
from utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
"""
content += "        return f\""
content += "{camel_case_to_snake_case(cls.__name__)}s\""
content += "\n\n"

# Запись в файл
with open(f"models/base.py", "w") as file:
    file.write(content)

print(f"Файл models/base.py успешно создан.")

# ===============================
# import sys
