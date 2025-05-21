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
from schemas.{ENTITY_NAME_low} import {ENTITY_NAME}Create, {ENTITY_NAME}Update, {ENTITY_NAME}Patch 


async def get_all_{ENTITY_NAME_low}(session: AsyncSession) -> Sequence[{ENTITY_NAME}]:
    stmt = select({ENTITY_NAME}).order_by({ENTITY_NAME}.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_{ENTITY_NAME_low}(session: AsyncSession, {ENTITY_NAME_low}_id: int) -> {ENTITY_NAME} | None:
    return await session.get({ENTITY_NAME}, {ENTITY_NAME_low}_id)


async def get_{ENTITY_NAME_low}s_by_field(session: AsyncSession, field_name: str, value: str) -> Sequence[{ENTITY_NAME}]:
    # Получаем атрибут модели по имени поля
    field = getattr({ENTITY_NAME}, field_name)
    stmt = select({ENTITY_NAME}).where(field == value)
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


async def update_{ENTITY_NAME_low}(
    session: AsyncSession,
    {ENTITY_NAME_low}: {ENTITY_NAME},
    {ENTITY_NAME_low}_update: {ENTITY_NAME}Update | {ENTITY_NAME}Patch,
    partial: bool = False,
) -> {ENTITY_NAME}:
    for name, value in {ENTITY_NAME_low}_update.model_dump(exclude_unset=partial).items():
        setattr({ENTITY_NAME_low}, name, value)
    await session.commit()
    return {ENTITY_NAME_low}


async def delete_{ENTITY_NAME_low}(session: AsyncSession, {ENTITY_NAME_low}: {ENTITY_NAME},) -> None:
    await session.delete({ENTITY_NAME_low})
    await session.commit()
    
'''

# Запись в файл
with open(f"crud/{ENTITY_NAME_low}.py", "w") as file:
    file.write(content)

print(f"Файл crud/{ENTITY_NAME.lower()}.py успешно сделан.")

# ===============================
# import sys

