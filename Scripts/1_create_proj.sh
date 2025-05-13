#!/bin/bash
echo "# ================================================="
echo "# === I. Подготовка проекта, установка пакетов. ==="
echo "# ================================================="

export PWD_SCRIPT=$PWD

echo
PROJECT_NAME="temft"
read -rp "=== Введите имя проекта ('Enter' - по умолчанию [$PROJECT_NAME]): " inp_tmp
if [ -n "$inp_tmp" ]; then
    PROJECT_NAME=$inp_tmp
else
    echo "Выбрано название проекта по умолчанию: $PROJECT_NAME."
fi
export PROJECT_NAME

echo
ENTITY_NAME="item"
read -rp "=== Введите имя сущности ('Enter' - по умолчанию [$ENTITY_NAME]): " inp_tmp
if [ -n "$inp_tmp" ]; then
    ENTITY_NAME=$inp_tmp    
else
    echo "Выбрано название сущности по умолчанию: $ENTITY_NAME."
fi
export ENTITY_NAME

echo
echo "=== Выберите версию Python: ==="
echo "1. python-3.8"
echo "2. python-3.9"
echo "3. python-3.10 (по умолчанию)"
echo "4. python-3.11"
echo "5. python-3.12"
echo "6. python-3.13"
echo "7. python-3.14"
read -rp "=== Введите номер пункта ('Enter' - по умолчанию [3] python-3.10): " num_tmp

if ! [[ "$num_tmp" =~ ^[0-9]+$ ]] || [ -z "$num_tmp" ] || [ "$num_tmp" -lt 1 ] || [ "$num_tmp" -gt 7 ]; then
    VER_PYTHON="3.10"
    echo "Выбрана версия Python по умолчанию: $VER_PYTHON"
else
    VER_PYTHON="3.$((7+num_tmp))"
    echo "Выбрана версия Python: $VER_PYTHON"
fi
export VER_PYTHON

echo
echo "==========================================================="
echo "Создается проект '$PROJECT_NAME' с сущностью '$ENTITY_NAME'"
echo "==========================================================="

mkdir "$PROJECT_NAME" && echo "Обший каталог '$PROJECT_NAME' создан" || exit 1
cd "$PROJECT_NAME" || exit 1
echo
echo "=== Инициализация UV и установка пакетов ==="

uv init --python $VER_PYTHON
uv add fastapi "uvicorn[standard]" "pydantic[email]" pydantic-settings
rm main.py
echo
mkdir "$PROJECT_NAME" && echo "Каталог проекта FastAPI '$PROJECT_NAME' создан" || exit 1

echo "import uvicorn
from fastapi import FastAPI
main_app = FastAPI()
if __name__ == '__main__':
    uvicorn.run('main:main_app')
" > ./"$PROJECT_NAME"/main.py
echo "Создан 'main.py''"

echo
echo "=== Коммитим проект ==="
pwd
cp ../Scripts/.gitignore ./
git init
git status
git add .
git commit -am "First commit"

echo
echo "=== Текущий каталог: $PWD ==="
echo "=== Текущая структуру: ==="
tree -a --dirsfirst -I '__pycache__|\.venv|\.git|\.idea'
echo
echo "Для запуска проекта перейдите в каталог: cd $PROJECT_NAME"
echo "И запустите: uv run python $PROJECT_NAME/main.py"
echo
echo "Запись переменных для скрипта в 'export_VARS.sh'"
cd "$PWD_SCRIPT"/Scripts || exit 1
{
echo "export PWD_SCRIPT=$PWD_SCRIPT"
echo "export PROJECT_NAME=$PROJECT_NAME"
echo "export ENTITY_NAME=$ENTITY_NAME"
echo "export VER_PYTHON=$VER_PYTHON"
} > export_VARS.sh
echo
echo "# ===================================="
echo "# === Завершение работы скрипта I. ==="
echo "# ===================================="
echo


#=======================================
#cd "$PWD_SCRIPT" || exit 1

#uv init --python 3.10
#uv init $PROJECT_NAME --python 3.10

#echo "export PWD_SCRIPT=$PWD_SCRIPT" > export_VARS.sh
#echo "export PROJECT_NAME=$PROJECT_NAME" >> export_VARS.sh
#echo "export ENTITY_NAME=$ENTITY_NAME" >> export_VARS.sh
#echo "export VER_PYTHON=$VER_PYTHON" >> export_VARS.sh






