#!/bin/bash
echo "# =========================================="
echo "# ===  II. Формирование структуры.       ==="
echo "# =========================================="

source ./Scripts/export_VARS.sh
echo "=== Переменные для скрипта: ==="
echo "=== Путь для скрипта: $PWD_SCRIPT ==="
echo "=== Имя проекта: $PROJECT_NAME, Сущность: $ENTITY_NAME, Python: $VER_PYTHON ==="

cd "$PWD_SCRIPT/$PROJECT_NAME" || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME/"; exit 1; }

mkdir api api/api_v1 core crud models models/mixins schemas utils
touch api/__init__.py api/api_v1/__init__.py "api/api_v1/$ENTITY_NAME.py"
touch core/config.py core/__init__.py
touch crud/__init__.py "crud/$ENTITY_NAME.py"
touch models/__init__.py models/mixins/__init__.py "models/$ENTITY_NAME.py"
touch schemas/__init__.py "schemas/$ENTITY_NAME.py"
touch utils/__init__.py
touch .env.template .env 

echo
cd "$PWD_SCRIPT/$PROJECT_NAME" || exit 1
echo "=== Текущий каталог: $PWD ==="
echo "=== Текущая структуру: ==="
tree -a --dirsfirst -I '__pycache__|\.venv|\.git|\.idea'

echo
echo "# ====================================="
echo "# === Завершение работы скрипта II. ==="
echo "# ====================================="
echo


#=======================================
#cd "$PWD_SCRIPT" || exit 1
