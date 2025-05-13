import sys

# Проверяем, передан ли аргумент
if len(sys.argv) != 2:
    print("Использование: python mk_file_schemas_ENTITY.py <ENTITY_NAME>")
    sys.exit(1)

ENTITY_NAME = sys.argv[1].capitalize()  # Получаем значение ENTITY_NAME из аргумента командной строки
ENTITY_NAME_low = ENTITY_NAME.lower()

content = f'''from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models import {ENTITY_NAME}
from schemas.{ENTITY_NAME_low} import {ENTITY_NAME}Create


async def get_all_{ENTITY_NAME_low}(session: AsyncSession) -> Sequence[{ENTITY_NAME}]:
    stmt = select({ENTITY_NAME}).order_by({ENTITY_NAME}.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_{ENTITY_NAME_low}(session: AsyncSession, {ENTITY_NAME_low}: {ENTITY_NAME}Create) -> {ENTITY_NAME}:
    try:
        {ENTITY_NAME_low} = {ENTITY_NAME}(**{ENTITY_NAME_low}.model_dump())
        session.add({ENTITY_NAME_low})
        await session.commit()
        await session.refresh({ENTITY_NAME_low})
        return {ENTITY_NAME_low}
    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e).lower():
        # if "uq_items_name" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                # detail="Item violates unique constraint"
                detail=f"Item with name '''
content += "'{"
content += f"{ENTITY_NAME_low}.name"
content += "}' "
content += f'''already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error"
        )

'''

# Запись в файл
with open(f"crud/{ENTITY_NAME.lower()}.py", "w") as file:
    file.write(content)

print(f"Файл crud/{ENTITY_NAME.lower()}.py успешно сделан.")

# ===============================
# import sys

