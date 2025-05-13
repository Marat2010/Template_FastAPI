#!/bin/bash
echo "# ==================================="
echo "# === VI. Схемы Pydantic и CRUD. === "
echo "# ==================================="

source ./Scripts/export_VARS.sh
echo "=== Переменные для скрипта: ==="
echo "=== Путь для скрипта: $PWD_SCRIPT ==="
echo "=== Имя проекта: $PROJECT_NAME, Сущность: $ENTITY_NAME, Python: $VER_PYTHON ==="

cd "$PWD_SCRIPT/$PROJECT_NAME/$PROJECT_NAME" || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME"; exit 1; }

echo
echo "Формирование файла schemas/$ENTITY_NAME.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_schemas_ENTITY.py "$ENTITY_NAME"

echo
echo "Формирование файла crud/$ENTITY_NAME.py"
python3 "$PWD_SCRIPT"/Scripts/mk_file_crud_ENTITY.py "$ENTITY_NAME"


#==========================================
echo
echo "=== Коммитим проект ==="
git add .
git commit -am "Setting up alembic, creating tables."

echo
echo "# ====================================="
echo "# === Завершение работы скрипта VI. ==="
echo "# ====================================="
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