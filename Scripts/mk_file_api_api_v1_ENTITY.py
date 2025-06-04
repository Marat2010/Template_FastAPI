import sys

# Проверяем, передан ли аргумент
if len(sys.argv) != 2:
    print("Использование: python mk_file_api_api_v1_ENTITY.py <ENTITY_NAME>")
    sys.exit(1)

ENTITY_NAME = sys.argv[1].capitalize()  # Получаем значение ENTITY_NAME из аргумента командной строки
ENTITY_NAME_low = ENTITY_NAME.lower()

content = f'''from datetime import datetime

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from crud import {ENTITY_NAME_low} as {ENTITY_NAME_low}s_crud
from .dependencies import {ENTITY_NAME_low}_by_id
from models import db_helper
from schemas.{ENTITY_NAME_low} import {ENTITY_NAME}Read, {ENTITY_NAME}Create, {ENTITY_NAME}Update, {ENTITY_NAME}Patch

router = APIRouter()


@router.get("", response_model=list[{ENTITY_NAME}Read])
async def get_{ENTITY_NAME_low}s(session: AsyncSession = Depends(db_helper.session_getter)):
    {ENTITY_NAME_low} = await {ENTITY_NAME_low}s_crud.get_all_{ENTITY_NAME_low}(session=session)
    return {ENTITY_NAME_low}


@router.get("/'''
content += "{"
content += f"{ENTITY_NAME_low}_id"
content += '}/",'
content += f'''response_model={ENTITY_NAME}Read)
async def get_{ENTITY_NAME_low}({ENTITY_NAME_low}: {ENTITY_NAME}Read = Depends({ENTITY_NAME_low}_by_id)):
    return {ENTITY_NAME_low}
    
    
@router.post("", response_model={ENTITY_NAME}Read)
async def create_{ENTITY_NAME_low}({ENTITY_NAME_low}_create: {ENTITY_NAME}Create,
                      session: AsyncSession = Depends(db_helper.session_getter)):
    return await {ENTITY_NAME_low}s_crud.create_{ENTITY_NAME_low}({ENTITY_NAME_low}={ENTITY_NAME_low}_create, session=session)


@router.put("/'''
content += "{"
content += f"{ENTITY_NAME_low}_id"
content += '}/"'
content += f''')
async def update_{ENTITY_NAME_low}({ENTITY_NAME_low}_update: {ENTITY_NAME}Update,
                      {ENTITY_NAME_low}: {ENTITY_NAME}Read = Depends({ENTITY_NAME_low}_by_id),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    return await {ENTITY_NAME_low}s_crud.update_{ENTITY_NAME_low}(
        {ENTITY_NAME_low}_update={ENTITY_NAME_low}_update,
        {ENTITY_NAME_low}={ENTITY_NAME_low},
        session=session)


@router.patch("/'''
content += "{"
content += f"{ENTITY_NAME_low}_id"
content += '}/"'
content += f''')
async def update_{ENTITY_NAME_low}_partial({ENTITY_NAME_low}_update: {ENTITY_NAME}Patch,
                              {ENTITY_NAME_low}: {ENTITY_NAME}Read = Depends({ENTITY_NAME_low}_by_id),
                              session: AsyncSession = Depends(db_helper.session_getter)):
    return await {ENTITY_NAME_low}s_crud.update_{ENTITY_NAME_low}(
        {ENTITY_NAME_low}_update={ENTITY_NAME_low}_update,        
        {ENTITY_NAME_low}={ENTITY_NAME_low},
        session=session,
        partial=True)


@router.delete("/'''
content += "{"
content += f"{ENTITY_NAME_low}_id"
content += '}/"'
content += f''', status_code=status.HTTP_204_NO_CONTENT)
async def delete_{ENTITY_NAME_low}({ENTITY_NAME_low}: {ENTITY_NAME}Read = Depends({ENTITY_NAME_low}_by_id),
                      session: AsyncSession = Depends(db_helper.session_getter)) -> None:
    await {ENTITY_NAME_low}s_crud.delete_{ENTITY_NAME_low}({ENTITY_NAME_low}={ENTITY_NAME_low}, session=session)


@router.get("/filter", response_model=list[{ENTITY_NAME}Read])
async def filter_{ENTITY_NAME_low}s(
        name: str | None = Query(None),
        description: str | None = Query(None),
        is_active: bool | None = Query(None),
        created_at_gt: datetime | None = Query(None, description='Пример: "2025-05-24" или "2025-05-24 09:03:00"'),
        created_at_lt: datetime | None = Query(None),
        session: AsyncSession = Depends(db_helper.session_getter)):
    filters = '''
content += '''{}
    if name:
        filters['name'] = name
    if description:
        filters['description'] = description
    if is_active is not None:
        filters['is_active'] = is_active

    time_filters = {}
    if created_at_gt:
        time_filters['created_at__gt'] = created_at_gt
    if created_at_lt:
        time_filters['created_at__lt'] = created_at_lt
'''
content += f'''
    {ENTITY_NAME_low} = await {ENTITY_NAME_low}s_crud.get_items_by_filters(
        session=session,
        filters=filters,
        time_filters=time_filters
    )
    return {ENTITY_NAME_low}


# ==========================================================
    # session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
    
'''


# Запись в файл
with open(f"api/api_v1/{ENTITY_NAME_low}.py", "w") as file:
    file.write(content)

print(f"Файл api/api_v1/{ENTITY_NAME_low}.py успешно сделан.")



