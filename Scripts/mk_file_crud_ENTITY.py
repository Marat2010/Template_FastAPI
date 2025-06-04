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

from api.api_v1.exceptions import {ENTITY_NAME}NameConflict
from models import {ENTITY_NAME}
from schemas.{ENTITY_NAME_low} import {ENTITY_NAME}Create, {ENTITY_NAME}Update, {ENTITY_NAME}Patch 

from utils.filters import apply_filters


async def get_all_{ENTITY_NAME_low}(session: AsyncSession) -> Sequence[{ENTITY_NAME}]:
    stmt = select({ENTITY_NAME}).order_by({ENTITY_NAME}.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_{ENTITY_NAME_low}(session: AsyncSession, {ENTITY_NAME_low}_id: int) -> {ENTITY_NAME} | None:
    return await session.get({ENTITY_NAME}, {ENTITY_NAME_low}_id)


async def is_name_exists(session: AsyncSession,
                         name: str,
                         exclude_{ENTITY_NAME_low}_id: int | None = None) -> bool:
    query = select({ENTITY_NAME}).where({ENTITY_NAME}.name == name)
    if exclude_{ENTITY_NAME_low}_id is not None:
        query = query.where({ENTITY_NAME}.id != exclude_{ENTITY_NAME_low}_id)
    return bool(await session.scalar(query))
    

async def create_{ENTITY_NAME_low}({ENTITY_NAME_low}: {ENTITY_NAME}Create, session: AsyncSession) -> {ENTITY_NAME}:
    # Проверка перед созданием
    if await is_name_exists(session, {ENTITY_NAME_low}.name):
        raise {ENTITY_NAME}NameConflict()

    db_{ENTITY_NAME_low} = {ENTITY_NAME}(**{ENTITY_NAME_low}.model_dump())
    session.add(db_{ENTITY_NAME_low})
    await session.commit()
    await session.refresh(db_{ENTITY_NAME_low})
    return db_{ENTITY_NAME_low}


async def update_{ENTITY_NAME_low}({ENTITY_NAME_low}_update: {ENTITY_NAME}Update | {ENTITY_NAME}Patch,
                      {ENTITY_NAME_low}: {ENTITY_NAME},
                      session: AsyncSession,
                      partial: bool = False, ) -> {ENTITY_NAME}:

    update_data = {ENTITY_NAME_low}_update.model_dump(exclude_unset=partial)

    if "name" in update_data and await is_name_exists(session, update_data["name"], {ENTITY_NAME_low}.id):
        raise {ENTITY_NAME}NameConflict()

    for name, value in update_data.items():
        setattr({ENTITY_NAME_low}, name, value)

    await session.commit()
    return {ENTITY_NAME_low}


async def delete_{ENTITY_NAME_low}({ENTITY_NAME_low}: {ENTITY_NAME}, session: AsyncSession) -> None:
    await session.delete({ENTITY_NAME_low})
    await session.commit()


async def get_items_by_filters(
    session: AsyncSession,
    filters: dict | None = None,
    time_filters: dict | None = None
) -> Sequence[{ENTITY_NAME}]:
    stmt = apply_filters({ENTITY_NAME}, filters, time_filters)
    result = await session.scalars(stmt)
    return result.all()
    
'''

# Запись в файл
with open(f"crud/{ENTITY_NAME_low}.py", "w") as file:
    file.write(content)

print(f"Файл crud/{ENTITY_NAME.lower()}.py успешно сделан.")

