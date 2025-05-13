#!/bin/bash
echo "# =========================================="
echo "# === III. Настройка общей конфигурации. === "
echo "# =========================================="

source ./Scripts/export_VARS.sh
echo "=== Переменные для скрипта: ==="
echo "=== Путь для скрипта: $PWD_SCRIPT ==="
echo "=== Имя проекта: $PROJECT_NAME, Сущность: $ENTITY_NAME, Python: $VER_PYTHON ==="

cd "$PWD_SCRIPT/$PROJECT_NAME/$PROJECT_NAME" || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME/$PROJECT_NAME"; exit 1; }

echo "=== Создаем файл core/config.py ==="
python3 "$PWD_SCRIPT"/Scripts/mk_file_core_config.py "$ENTITY_NAME"

echo
USER_BD=$USER
read -rp "=== Введите имя пользователя для БД Postgres ('Enter' - по умолчанию [$USER_BD]): " inp_tmp
if [ -n "$inp_tmp" ]; then
    USER_BD=$inp_tmp
else
    echo "Выбрано имя пользователя для БД по умолчанию: $USER_BD."
fi
export USER_BD

echo
PASSWD_BD=1
read -rp "=== Введите пароль для пользователя БД Postgres ('Enter' - по умолчанию [$PASSWD_BD]): " inp_tmp
if [ -n "$inp_tmp" ]; then
    PASSWD_BD=$inp_tmp
else
    echo "Выбран пароль для пользователя БД по умолчанию: $PASSWD_BD."
fi
export PASSWD_BD

echo
echo "=== Формирование файлов .env.template и .env ==="
echo "APP_CONFIG__DB__URL=postgresql+asyncpg://user:pwd@localhost:5432/app
APP_CONFIG__DB__ECHO=1
" > ./.env.template

echo "APP_CONFIG__DB__URL=postgresql+asyncpg://$USER_BD:$PASSWD_BD@localhost:5434/$PROJECT_NAME
APP_CONFIG__DB__ECHO=1
" > ./.env

echo
echo "=== Коммитим проект ==="
# git status
git add .
git commit -am "Structure and setting up general configuration"
echo
echo "Запись переменных для скрипта в 'export_VARS.sh'"
cd "$PWD_SCRIPT"/Scripts || exit 1
echo "export USER_BD=$USER_BD" >> export_VARS.sh
echo "export PASSWD_BD=$PASSWD_BD" >> export_VARS.sh
echo
echo "# ======================================"
echo "# === Завершение работы скрипта III. ==="
echo "# ======================================"
echo


#=======================================
#echo
#cd "$PWD_SCRIPT/$PROJECT_NAME" || exit 1
#echo "=== Текущий каталог: $PWD ==="
#echo "=== Текущая структуру: ==="
#tree -a --dirsfirst -I '__pycache__|\.venv|\.git|\.idea'
#=======================================
#cd "$PWD_SCRIPT" || exit 1
