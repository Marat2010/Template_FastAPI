#!/bin/bash
echo "============ Проект ==========="
# --- Пути для скриптов и шаблонов ---
SCRIPTS_DIR="Scripts_v2"

PWD_SCRIPT="$(dirname "$0")"
FULL_TEMPLATES_DIR="$PWD_SCRIPT/$TEMPLATES_DIR"
FULL_SCRIPTS_DIR="$PWD_SCRIPT/$SCRIPTS_DIR"


PROJECT_DIR="templ_fa"
echo "== проект дир= $PROJECT_DIR"

FULL_PROJECT_DIR="$PWD_SCRIPT/$PROJECT_DIR"
echo "== Фулл проект дир= $FULL_PROJECT_DIR"

ls -al $PROJECT_DIR 

echo "==============================="
echo "==============================="

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
" > "$PROJECT_DIR/.env.template"
#" > ./.env.template

echo "APP_CONFIG__DB__URL=postgresql+asyncpg://$USER_BD:$PASSWD_BD@localhost:5434/$PROJECT_NAME
APP_CONFIG__DB__ECHO=0
" > "$PROJECT_DIR/.env"
#" > ./.env

echo "================================="



