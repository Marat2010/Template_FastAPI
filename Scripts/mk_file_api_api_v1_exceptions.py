import sys

# Проверяем, передан ли аргумент
if len(sys.argv) != 2:
    print("Использование: python mk_file_schemas_ENTITY.py <ENTITY_NAME>")
    sys.exit(1)

ENTITY_NAME = sys.argv[1].capitalize()  # Получаем значение ENTITY_NAME из аргумента командной строки
ENTITY_NAME_low = ENTITY_NAME.lower()

content = f'''from fastapi import HTTPException, status


class {ENTITY_NAME}NameConflict(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item with this name already exists"
        )

'''

# Запись в файл
with open(f"api/api_v1/exceptions.py", "w") as file:
    file.write(content)

print(f"Файл api/api_v1/exceptions.py успешно сделан.")

