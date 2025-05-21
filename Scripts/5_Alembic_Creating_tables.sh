#!/bin/bash
echo "# =============================================="
echo "# === V. Настройка alembic, создание таблиц. === "
echo "# =============================================="

source ./Scripts/export_VARS.sh
echo "=== Переменные для скрипта: ==="
echo "=== Путь для скрипта: $PWD_SCRIPT ==="
echo "=== Имя проекта: $PROJECT_NAME, Сущность: $ENTITY_NAME, Python: $VER_PYTHON ==="

cd "$PWD_SCRIPT/$PROJECT_NAME/" || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME"; exit 1; }
#cd "$PWD_SCRIPT/$PROJECT_NAME/$PROJECT_NAME" || { echo "Не удалось перейти в каталог проекта $PROJECT_NAME"; exit 1; }

echo
echo "=== Инициализируем  alembic ==="
uv run alembic init -t async alembic

echo
echo "=== Раскомментируем file_template и black в 'alembic.ini'==="
cp alembic.ini alembic.ini_bak
sed -i 's/^# file_template = /file_template = /' alembic.ini

sed -i 's/^# hooks = black/hooks = black/' alembic.ini
sed -i 's/^# black.type /black.type /' alembic.ini
sed -i 's/^# black.entrypoint /black.entrypoint /' alembic.ini
sed -i 's/^# black.options /black.options /' alembic.ini

echo
echo "=== Установим black для режима dev ==="
uv add --dev black

echo
echo "=== Редактируем alembic/env.py ==="

cp alembic/env.py alembic/env.py_bak
sed -i 's/^target_metadata = None/target_metadata = Base.metadata/' alembic/env.py

sed -i '/from alembic import context/a from models import Base\nfrom core.config import settings' alembic/env.py

sed -i '/target_metadata = Base.metadata/a\
config.set_main_option("sqlalchemy.url", str(settings.db.url))' alembic/env.py

echo
echo "=== Делаем первую миграцию alembic ==="
uv run alembic revision --autogenerate -m "create $ENTITY_NAME table"
echo "=== Применяем эту миграцию ==="
uv run alembic upgrade head
echo
echo "=== Проверьте БД ($PROJECT_NAME), должна быть создана таблица: $ENTITY_NAME's ==="
read -rp "Для продолжения нажмите 'Enter'"
echo
echo "=== Коммитим проект ==="
# git status
git add .
git commit -am "Setting up alembic, creating tables."

echo
echo "# ===================================="
echo "# === Завершение работы скрипта V. ==="
echo "# ===================================="
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