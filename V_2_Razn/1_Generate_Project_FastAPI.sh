#!/bin/bash

validate_entity_name() {
    if [[ ! "$1" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        echo "Ошибка: имя сущности может содержать только буквы, цифры, дефисы и подчёркивания"
        exit 1
    fi
}

# --- Параметры по умолчанию ---
DEFAULT_PROJECT_NAME="templ_fa"
DEFAULT_ENTITY_NAME="book"
TEMPLATES_DIR="template_FA"
SCRIPTS_DIR="Scripts_v2"

# --- Запрос имени сущности ---
if [ -z "$1" ]; then
    echo
    read -rp "=== Введите имя сущности (Enter - по умолчанию [$DEFAULT_ENTITY_NAME]): " ENTITY_NAME
    if [ -z "$ENTITY_NAME" ]; then
        ENTITY_NAME="$DEFAULT_ENTITY_NAME"
        echo "Выбрано имя сущности по умолчанию: $ENTITY_NAME."
    fi
else
    ENTITY_NAME="$1"  # Используем переданный аргумент
fi

validate_entity_name "$ENTITY_NAME"

# --- Запрос имени проекта ---
echo
read -rp "=== Введите имя проекта (Enter - по умолчанию [$DEFAULT_PROJECT_NAME]): " PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="$DEFAULT_PROJECT_NAME"
    echo "Выбрано название проекта по умолчанию: $PROJECT_NAME."
fi

# --- Создание папки проекта ---
PROJECT_DIR="$PROJECT_NAME"
mkdir -p "$PROJECT_DIR"
echo "Проект создан в папке: $PROJECT_DIR"

select_python_version() {
    local num_tmp
    # Сначала выводим меню
    echo "=== Выберите версию Python: ===" >&2
    echo "1. python-3.8" >&2
    echo "2. python-3.9" >&2
    echo "3. python-3.10 (по умолчанию)" >&2
    echo "4. python-3.11" >&2
    echo "5. python-3.12" >&2
    echo "6. python-3.13" >&2
    echo "7. python-3.14" >&2

    # Затем запрашиваем ввод
    read -rp "=== Введите номер пункта ('Enter' - по умолчанию [3] python-3.10): " num_tmp >&2

    # Возвращаем только версию (без лишних сообщений)
    if ! [[ "$num_tmp" =~ ^[0-9]+$ ]] || [ -z "$num_tmp" ] || [ "$num_tmp" -lt 1 ] || [ "$num_tmp" -gt 7 ]; then
        echo "3.10"
    else
        echo "3.$((num_tmp+7))"
    fi
}

echo "=== Выбор версии Python ==="
PYTHON_VERSION=$(select_python_version)
echo "Выбрана версия Python: $PYTHON_VERSION"

#export PYTHON_VERSION  # Делаем переменную доступной для дочерних процессов

# --- Пути для скриптов и шаблонов ---
PWD_SCRIPT="$(dirname "$0")"
FULL_TEMPLATES_DIR="$PWD_SCRIPT/$TEMPLATES_DIR"
FULL_SCRIPTS_DIR="$PWD_SCRIPT/$SCRIPTS_DIR"

# --- Список шаблонов ---
TEMPLATES=(
    "main.py.template"
    "schemas/{{ENTITY_NAME}}.py.template"
    "schemas/__init__.py.template"
    "crud/{{ENTITY_NAME}}.py.template"
    "crud/__init__.py.template"
    "core/config.py.template"
    "core/logger.py.template"
    "core/__init__.py.template"
    "core/middleware/http_logging.py.template"
    "utils/case_converter.py.template"
    "utils/db.py.template"
    "utils/filters.py.template"
    "utils/__init__.py.template"
    "api/__init__.py.template"
    "api/api_v1/__init__.py.template"
    "api/api_v1/{{ENTITY_NAME}}.py.template"
    "api/api_v1/dependencies.py.template"
    "api/api_v1/exceptions.py.template"
    "models/{{ENTITY_NAME}}.py.template"
    "models/__init__.py.template"
    "models/db_helper.py.template"
    "models/base.py.template"
    "models/mixins/int_id_pk.py.template"
    "models/mixins/__init__.py.template"
    "pyproject.toml.template"
    ".python-version.template"
)

# --- Генерация файлов ---
echo
echo "=== Генерация файлов для сущности $ENTITY_NAME ==="

for template in "${TEMPLATES[@]}"; do
    echo "Создаем файл из шаблона $template..."
    python3 "$FULL_SCRIPTS_DIR/mk_file_from_template.py" \
      "$ENTITY_NAME" \
      "$template" \
      "$PROJECT_DIR" \
      "$FULL_TEMPLATES_DIR" \
      "$PROJECT_NAME" \
      "$PYTHON_VERSION"
done

echo "Готово! Файлы созданы в папке $PROJECT_DIR."


#========= mk_DB_alembic.sh ========================



#=================================
#      "$LOG_FILE_MAX_SIZE" \
#      "$LOG_FILE_BACKUP_COUNT"
#===============================
#LOG_FILE_MAX_SIZE=$((10 * 1024 * 1024))  # 10 MB
#LOG_FILE_BACKUP_COUNT=5
