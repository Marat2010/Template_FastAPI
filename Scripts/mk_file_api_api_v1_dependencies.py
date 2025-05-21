import sys

# Проверяем, передан ли аргумент
if len(sys.argv) != 2:
    print("Использование: python mk_file_api_api_v1_dependencies.py <ENTITY_NAME>")
    sys.exit(1)

ENTITY_NAME = sys.argv[1].capitalize()  # Получаем значение ENTITY_NAME из аргумента командной строки
ENTITY_NAME_low = ENTITY_NAME.lower()

content = f'''from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper, {ENTITY_NAME}
from crud import {ENTITY_NAME_low} as {ENTITY_NAME_low}s_crud


async def {ENTITY_NAME_low}_by_id(
    {ENTITY_NAME_low}_id: Annotated[int, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> {ENTITY_NAME}:
    {ENTITY_NAME_low} = await {ENTITY_NAME_low}s_crud.get_{ENTITY_NAME_low}(session=session, {ENTITY_NAME_low}_id={ENTITY_NAME_low}_id)
    if {ENTITY_NAME_low}:
        return {ENTITY_NAME_low}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{ENTITY_NAME} id: '''
content += "{"
content += f"{ENTITY_NAME_low}_id"
content += "} "
content += '''not found!",
    )


'''


# Запись в файл
with open(f"api/api_v1/dependencies.py", "w") as file:
    file.write(content)

print(f"Файл api/api_v1/dependencies.py успешно сделан.")