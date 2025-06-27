#!/bin/bash

# --- Constants ---
DEFAULT_PROJECT_NAME="templ_fa"
DEFAULT_ENTITY_NAME="book"
TEMPLATES_DIR="template_FA"
SCRIPTS_DIR="Scripts_v2"

# --- Functions ---

# Validate entity name (letters, numbers, underscores, hyphens)
validate_entity_name() {
    if [[ ! "$1" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        echo "Error: Entity name can only contain letters, numbers, hyphens and underscores" >&2
        exit 1
    fi
}

# Python version selection menu
select_python_version() {
    local version_map=(
        ["1"]="3.8"
        ["2"]="3.9"
        ["3"]="3.10"
        ["4"]="3.11"
        ["5"]="3.12"
        ["6"]="3.13"
        ["7"]="3.14"
    )

    echo "=== Select Python Version ===" >&2
    for i in "${!version_map[@]}"; do
        echo "$i. python-${version_map[$i]}" >&2
    done

    read -rp "Enter choice [3]: " choice
    echo "${version_map[${choice:-3}]:-3.10}"
}

#===============================
# Select database type (Docker or existing)
select_database_type() {
    echo
    echo "========================================================================="
    echo "            Настройка подключения к PostgreSQL"
    echo "========================================================================="
    echo "1. Использовать существующий Postgres сервер"
    echo "2. Создать новый Postgres сервер в Docker (рекомендуется для разработки)"
    echo "========================================================================="

    while true; do
        read -rp "Выберите вариант [1/2]: " db_choice
        case "${db_choice}" in
            1)
                echo "Используем существующий Postgres сервер"
                return 1
                ;;
            2)
                echo "Создаем Postgres сервер в Docker"
                return 2
                ;;
            *)
                echo "Неверный выбор, попробуйте снова"
                ;;
        esac
    done
}

# Database connection setup
setup_database_connection() {
    select_database_type
    db_type=$?

    # Common credentials
    echo
    read -rp "Введите имя пользователя Postgres [${USER}]: " DB_USER
    DB_USER="${DB_USER:-$USER}"

    read -rp "Введите пароль пользователя [1]: " DB_PASSWORD
    DB_PASSWORD="${DB_PASSWORD:-1}"

    read -rp "Введите имя базы данных [${PROJECT_NAME}]: " DB_NAME
    DB_NAME="${DB_NAME:-$PROJECT_NAME}"

    if [ $db_type -eq 1 ]; then
        # Existing server (остаётся без изменений)
        ...
    else
        # Настройка Docker
        DB_HOST="postgres"  # Важно: используем имя сервиса для внутреннего доступа
        DB_PORT="5432"

        read -rp "Введите внешний порт для Docker Postgres [5434]: " EXTERNAL_DB_PORT
        EXTERNAL_DB_PORT="${EXTERNAL_DB_PORT:-5434}"

        # 1. Удаляем старый контейнер
        if docker ps -a --format '{{.Names}}' | grep -q "^${PROJECT_NAME}-postgres$"; then
            echo "Удаляем старый контейнер Postgres..."
            docker rm -f "${PROJECT_NAME}-postgres" >/dev/null
            docker volume rm "${PROJECT_NAME}_pg_data" >/dev/null 2>&1 || true
        fi

        # 2. Генерируем docker-compose.yml
        cat > "$PROJECT_DIR/docker-compose.yml" <<EOL
version: '3.8'

services:
  postgres:
    image: postgres:17.0-alpine
    container_name: "${PROJECT_NAME}-postgres"
    environment:
      POSTGRES_DB: "${DB_NAME}"
      POSTGRES_USER: "${DB_USER}"
      POSTGRES_PASSWORD: "${DB_PASSWORD}"
    ports:
      - "${EXTERNAL_DB_PORT}:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 5s
      timeout: 5s
      retries: 10
    restart: unless-stopped

volumes:
  pg_data:
    name: "${PROJECT_NAME}_pg_data"
EOL

        # 3. Запускаем контейнер
        echo "Запускаем Postgres в Docker..."
        (cd "$PROJECT_DIR" && docker compose up -d)

        # 4. Ждем инициализации
        echo "Ожидаем готовности Postgres (15-30 сек)..."
        local container_name="${PROJECT_NAME}-postgres"

        timeout 30s bash -c "until docker inspect -f '{{.State.Health.Status}}' \"$container_name\" | grep -q \"healthy\"; do sleep 2; echo 'Ожидание...'; done" || {
            echo "Ошибка: Postgres не запустился. Проверьте логи:"
            docker logs "$container_name"
            exit 1
        }

        echo "Готово! База данных '$DB_NAME' создана."
    fi

    echo
    echo "===================================================================="
    echo " Настройки подключения к PostgreSQL:"
    echo "--------------------------------------------------------------------"
    echo " Хост:        $DB_HOST"
    echo " Порт:        $DB_PORT"
    [ $db_type -eq 2 ] && echo " Внешний порт: $EXTERNAL_DB_PORT"
    echo " База данных: $DB_NAME"
    echo " Пользователь: $DB_USER"
    echo " Пароль:      $DB_PASSWORD"
    [ $db_type -eq 2 ] && echo " (Docker контейнер: ${PROJECT_NAME}-pg)"
    echo "===================================================================="
}

# Generate .env files (updated)
generate_env_files() {
    echo "=== Создание файлов .env ==="

    # Template with placeholders
    sed "s/{{DB_USER}}/user/g; s/{{DB_PASSWORD}}/pwd/g; s/{{DB_HOST}}/localhost/g; s/{{DB_PORT}}/5432/g; s/{{DB_NAME}}/db_name/g" \
        "$FULL_TEMPLATES_DIR/.env.template" > "$PROJECT_DIR/.env.template"

    # Actual .env with real credentials
    sed "s/{{DB_USER}}/$DB_USER/g; s/{{DB_PASSWORD}}/$DB_PASSWORD/g; s/{{DB_HOST}}/$DB_HOST/g; s/{{DB_PORT}}/$DB_PORT/g; s/{{DB_NAME}}/$DB_NAME/g" \
        "$FULL_TEMPLATES_DIR/.env.template" > "$PROJECT_DIR/.env"
}

#===============================

# Alembic initialization
setup_alembic() {
    echo "=== Initializing Alembic ==="

    # Сначала создаем .env файл с правильными настройками
    cat > "$PROJECT_DIR/.env" <<EOL
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=${DB_HOST}
DB_PORT=${DB_PORT}
DB_NAME=${DB_NAME}
EOL

    # Инициализируем Alembic
    (cd "$PROJECT_DIR" && \
     uv run alembic init -t async alembic && \
     cp "$FULL_TEMPLATES_DIR/alembic.ini" "$PROJECT_DIR/" && \
     cp -R "$FULL_TEMPLATES_DIR/alembic" "$PROJECT_DIR/")

    # Применяем миграции
    (cd "$PROJECT_DIR" && \
     uv run alembic revision --autogenerate -m "init" && \
     uv run alembic upgrade head)
}

# --- Main Script ---

# 1. Get entity name
if [ -z "$1" ]; then
    read -rp "Enter entity name [$DEFAULT_ENTITY_NAME]: " ENTITY_NAME
    ENTITY_NAME="${ENTITY_NAME:-$DEFAULT_ENTITY_NAME}"
else
    ENTITY_NAME="$1"
fi
validate_entity_name "$ENTITY_NAME"

# 2. Get project name
read -rp "Enter project name [$DEFAULT_PROJECT_NAME]: " PROJECT_NAME
PROJECT_NAME="${PROJECT_NAME:-$DEFAULT_PROJECT_NAME}"

# 3. Create project directory
PROJECT_DIR="$PROJECT_NAME"
mkdir -p "$PROJECT_DIR" || { echo "Failed to create project directory"; exit 1; }

# 4. Select Python version
PYTHON_VERSION=$(select_python_version)
echo "Selected Python version: $PYTHON_VERSION"

# 5. Set paths
SCRIPT_DIR="$(dirname "$0")"
FULL_TEMPLATES_DIR="$SCRIPT_DIR/$TEMPLATES_DIR"
FULL_SCRIPTS_DIR="$SCRIPT_DIR/$SCRIPTS_DIR"

# 6. Database setup
setup_database_connection
generate_env_files

# 7. Generate project files
echo "=== Generating project files ==="
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

for template in "${TEMPLATES[@]}"; do
    python3 "$FULL_SCRIPTS_DIR/mk_file_from_template.py" \
        "$ENTITY_NAME" \
        "$template" \
        "$PROJECT_DIR" \
        "$FULL_TEMPLATES_DIR" \
        "$PROJECT_NAME" \
        "$PYTHON_VERSION" \
        "$DB_USER" \
        "$DB_PASSWORD"
done

# 8. Initialize Alembic
setup_alembic

echo "=== Project setup complete ==="
echo "Project directory: $PROJECT_DIR"



#====================================
#====================================
## --- Список шаблонов ---
#TEMPLATES=(
#    "main.py.template"
#    "schemas/{{ENTITY_NAME}}.py.template"
#    "schemas/__init__.py.template"
#    "crud/{{ENTITY_NAME}}.py.template"
#    "crud/__init__.py.template"
#    "core/config.py.template"
#    "core/logger.py.template"
#    "core/__init__.py.template"
#    "core/middleware/http_logging.py.template"
#    "utils/case_converter.py.template"
#    "utils/db.py.template"
#    "utils/filters.py.template"
#    "utils/__init__.py.template"
#    "api/__init__.py.template"
#    "api/api_v1/__init__.py.template"
#    "api/api_v1/{{ENTITY_NAME}}.py.template"
#    "api/api_v1/dependencies.py.template"
#    "api/api_v1/exceptions.py.template"
#    "models/{{ENTITY_NAME}}.py.template"
#    "models/__init__.py.template"
#    "models/db_helper.py.template"
#    "models/base.py.template"
#    "models/mixins/int_id_pk.py.template"
#    "models/mixins/__init__.py.template"
#    "pyproject.toml.template"
#    ".python-version.template"
##    ".env.template"
##    "docker-compose.yml.template"
#)
#===============================
#===============================
#
## Database credentials setup
#setup_database_credentials() {
#    echo
#    echo "========================================================================="
#    echo "Введите данные для своего Postgres сервера, если будете использовать его,"
#    echo "иначе, ниже будет предложено создать Postgres сервер в докере "
#    echo "========================================================================="
#    read -rp "Enter Postgres username [${USER}]: " DB_USER
#    DB_USER="${DB_USER:-$USER}"
#
#    read -rp "Enter Postgres password [1]: " DB_PASSWORD
#    DB_PASSWORD="${DB_PASSWORD:-1}"
#
#    read -rp "Enter Postgres host [localhost]: " DB_HOST
#    DB_HOST="${DB_HOST:-localhost}"
#
#    read -rp "Enter Postgres port [5434]: " DB_PORT
#    DB_PORT="${DB_PORT:-5434}"
#
#    echo "Database credentials:"
#    echo " - User: $DB_USER"
#    echo " - Password: $DB_PASSWORD"
#    echo " - Host: $DB_HOST"
#    echo " - Port: $DB_PORT"
#    echo " - Database: $PROJECT_NAME"
#}
#
## Generate .env files
#generate_env_files() {
#    echo "=== Generating .env files ==="
#
#    # Template with placeholders
#    sed "s/{{DB_USER}}/user/g; s/{{DB_PASSWORD}}/pwd/g; s/{{DB_HOST}}/localhost/g; s/{{DB_PORT}}/5432/g; s/{{PROJECT_NAME}}/db_name/g" \
#        "$FULL_TEMPLATES_DIR/.env.template" > "$PROJECT_DIR/.env.template"
#
#    # Actual .env with real credentials
#    sed "s/{{DB_USER}}/$DB_USER/g; s/{{DB_PASSWORD}}/$DB_PASSWORD/g; s/{{DB_HOST}}/$DB_HOST/g; s/{{DB_PORT}}/$DB_PORT/g; s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
#        "$FULL_TEMPLATES_DIR/.env.template" > "$PROJECT_DIR/.env"
#}
#
## Docker setup
#setup_docker() {
#    read -rp "Run Postgres in Docker? [Y/n]: " choice
#    case "${choice:-Y}" in
#        [nN])
#            echo "Skipping Docker setup"
#            echo "========================================================================="
#            echo "Не забудьте создать БД '$PROJECT_NAME' вручную на вашем Postgres сервере."
#            echo "Если БД с таким именем не будет, то Alembic не сможет создать таблицы"
#            echo "========================================================================="
#            read -rp "Для продолжения нажмите 'Enter'"
#            return
#            ;;
#        *)
#            echo "=== Setting up Docker ==="
#            sed "s/{{PROJECT_NAME}}/$PROJECT_NAME/g; s/{{DB_USER}}/$DB_USER/g; s/{{DB_PASSWORD}}/$DB_PASSWORD/g; s/{{DB_PORT}}/$DB_PORT/g" \
#                "$FULL_TEMPLATES_DIR/docker-compose.yml.template" > "$PROJECT_DIR/docker-compose.yml"
#
#            (cd "$PROJECT_DIR" && docker compose up -d pg)
#
#            echo "Database connection info:"
#            echo " - Host: localhost"
#            echo " - Port: $DB_PORT"
#            echo " - Database: $PROJECT_NAME"
#            echo " - User: $DB_USER"
#            echo " - Password: $DB_PASSWORD"
#            ;;
#    esac
#}
#===============================
## 6. Database setup
#setup_database_credentials
#generate_env_files
#setup_docker
#===============================
#LOG_FILE_MAX_SIZE=$((10 * 1024 * 1024))  # 10 MB
#LOG_FILE_BACKUP_COUNT=5
