#!/bin/bash
echo "# ============================================"
echo "# === IV. Настройка БД Postgres и моделей. === "
echo "# ============================================"

source ./Scripts/export_VARS.sh
echo "=== Переменные для скрипта: ==="
echo "=== Путь для скрипта: $PWD_SCRIPT ==="
echo "=== Имя проекта: $PROJECT_NAME, Сущность: $ENTITY_NAME, Python: $VER_PYTHON ==="

cd "$PWD_SCRIPT/$PROJECT_NAME" || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME"; exit 1; }

echo
echo "=== Установка пакетов sqlalchemy, asyncpg, alembic ==="
uv add "sqlalchemy[asyncio]" asyncpg alembic

echo
read -rp "=== Запустить Postgres сервер в докере Y/n ('Enter' - по умолчанию [Yes]): " inp_tmp
if [ -z "$inp_tmp" ] || [[ "$inp_tmp" =~ ^[Yy]$ ]]; then
    echo
    echo "=== Создается файл ../docker-compose.yml ==="
    python3 "$PWD_SCRIPT"/Scripts/mk_file_docker.py "$PROJECT_NAME" "$USER_BD" "$PASSWD_BD"
    echo
    docker compose up -d pg
    echo
    echo "__ Postgres сервер запущен в докере. __"
    echo "Подключитесь к серверу под ранее заданным пользователем ($USER_BD), и паролем."
    echo "Имя БД: $PROJECT_NAME, хост: localhost, порт: 5434"
else
    echo "__ Postgres сервер в докере не будет запущен!!! ___"
    echo "Подключитесь к своему серверу под ранее заданным пользователем ($USER_BD) и паролем,"
    echo "и создайте БД с названием: $PROJECT_NAME"
fi
echo
read -rp "Если прочитали нажмите 'Enter'"

cd "$PWD_SCRIPT/$PROJECT_NAME/" || exit 1
#cd "$PWD_SCRIPT/$PROJECT_NAME/$PROJECT_NAME" || exit 1

echo
echo "Формирование файла models/base.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_models_base.py

echo
echo "Формирование файла utils/case_converter.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_utils_case_converter.py

echo
echo "Формирование файла utils/__init__.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_utils__init.py

echo
echo "Формирование файла models/db_helper.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_models_db_helper.py

echo
echo "Формирование файла для сущности models/$ENTITY_NAME.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_models_ENTITY.py "$ENTITY_NAME"

echo
echo "Формирование файла models/mixins/int_id_pk.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_models_mixins_int_id_pk.py

echo
echo "Формирование файла models/__init__.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_models___init.py "$ENTITY_NAME"

echo
echo "=== Коммитим проект ==="
# git status
git add .
git commit -am "Preparing Postgres DB, Item model, Base, db_helper"

echo
echo "# ====================================="
echo "# === Завершение работы скрипта IV. ==="
echo "# ====================================="
echo


#=======================================
#poetry add "sqlalchemy[asyncio]" asyncpg alembic
#=======================================
#{
#echo "__all__ = ("
#echo '    "camel_case_to_snake_case",'
#echo ")"
#echo
#echo "from .case_converter import camel_case_to_snake_case"
#} > utils/__init__.py

#=======================================
#cd "$PWD_SCRIPT/$PROJECT_NAME/$PROJECT_NAME" || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME/$PROJECT_NAME"; exit 1; }
#=======================================
#cd "$PWD_SCRIPT/$PROJECT_NAME" && echo "Успешно перешли в каталог" || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME"; exit 1; }
#((cd "$PWD_SCRIPT/$PROJECT_NAME") && echo "Успешно перешли в каталог") || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME"; exit 1; }
#cd "$PWD_SCRIPT/$PROJECT_NAME" && echo "Успешно перешли в каталог" || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME"; exit 1; }
#=======================================
#echo
#cd "$PWD_SCRIPT/$PROJECT_NAME" || exit 1
#echo "=== Текущий каталог: $PWD ==="
#echo "=== Текущая структуру: ==="
#tree -a --dirsfirst -I '__pycache__|\.venv|\.git|\.idea'
#=======================================
#cd "$PWD_SCRIPT" || exit 1
#echo
#echo "=== Комимтим проект ==="
#git status
#git add .
#git commit -m "Structure and setting up general configuration"
