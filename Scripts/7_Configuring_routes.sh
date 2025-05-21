#!/bin/bash
echo "# ================================="
echo "# === VII. Настройка маршрутов. === "
echo "# ================================="

source ./Scripts/export_VARS.sh
echo "=== Переменные для скрипта: ==="
echo "=== Путь для скрипта: $PWD_SCRIPT ==="
echo "=== Имя проекта: $PROJECT_NAME, Сущность: $ENTITY_NAME, Python: $VER_PYTHON ==="

cd "$PWD_SCRIPT/$PROJECT_NAME/" || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME"; exit 1; }
#cd "$PWD_SCRIPT/$PROJECT_NAME/$PROJECT_NAME" || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME"; exit 1; }

echo
echo "Формирование файла api/api_v1/$ENTITY_NAME.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_api_api_v1_ENTITY.py "$ENTITY_NAME"

echo
echo "Формирование файла api/api_v1/dependencies.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_api_api_v1_dependencies.py "$ENTITY_NAME"

echo
echo "Формирование файла api/api_v1/__init__.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_api_api_v1___init.py "$ENTITY_NAME"

echo
echo "Формирование файла api/__init__.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_api___init.py

echo
echo "Формирование файла main.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_main.py "$ENTITY_NAME"

echo
echo "=== Установка пакета ORJSONResponse ==="
uv add orjson

echo
echo "=== Коммитим проект ==="
git add .
git commit -am "Configuring routes."

echo
echo "# ======================================"
echo "# === Завершение работы скрипта VII. ==="
echo "# ======================================"
echo


#====================================
#====================================
#sed -i '/from alembic import context/a\
#from models import Base\
#from core.config import settings' alembic/env.py

#sed -i '/from alembic import context/a \
#from models import Base\n\
#from core.config import settings' alembic/env.py

#sed -i '/from alembic import context/a from models import Base\nfrom core.config import settings' alembic/env.py
#====================================