import sys

# Проверяем, передан ли аргумент
if len(sys.argv) != 2:
    print("Использование: python mk_file_schemas_ENTITY.py <ENTITY_NAME>")
    sys.exit(1)

ENTITY_NAME = sys.argv[1].capitalize()  # Получаем значение ENTITY_NAME из аргумента командной строки
ENTITY_NAME_low = ENTITY_NAME.lower()

content = f'''from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import {ENTITY_NAME_low} as {ENTITY_NAME_low}s_crud
from models import db_helper
from schemas.{ENTITY_NAME_low} import {ENTITY_NAME}Read, {ENTITY_NAME}Create

router = APIRouter()

@router.get("", response_model=list[{ENTITY_NAME}Read])
async def get_{ENTITY_NAME_low}s(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    # session: AsyncSession = Depends(db_helper.session_getter),
    {ENTITY_NAME_low} = await {ENTITY_NAME_low}s_crud.get_all_{ENTITY_NAME_low}(session=session)
    return {ENTITY_NAME_low}

@router.post("", response_model={ENTITY_NAME}Read)
async def create_{ENTITY_NAME_low}(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                    {ENTITY_NAME_low}_create: {ENTITY_NAME}Create):
    {ENTITY_NAME_low} = await {ENTITY_NAME_low}s_crud.create_{ENTITY_NAME_low}(session=session, {ENTITY_NAME_low}={ENTITY_NAME_low}_create)
    return {ENTITY_NAME_low}

'''


# Запись в файл
with open(f"api/api_v1/{ENTITY_NAME_low}.py", "w") as file:
    file.write(content)

print(f"Файл api/api_v1/{ENTITY_NAME_low}.py успешно сделан.")



