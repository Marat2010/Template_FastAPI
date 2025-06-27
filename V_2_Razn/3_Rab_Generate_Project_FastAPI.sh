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

# Database credentials setup
setup_database_credentials() {
    echo
    echo "========================================================================="
    echo "Введите данные для своего Postgres сервера, если будете использовать его,"
    echo "иначе, ниже будет предложено создать Postgres сервер в докере "
    echo "========================================================================="
    read -rp "Enter Postgres username [${USER}]: " DB_USER
    DB_USER="${DB_USER:-$USER}"

    read -rp "Enter Postgres password [1]: " DB_PASSWORD
    DB_PASSWORD="${DB_PASSWORD:-1}"

    read -rp "Enter Postgres host [localhost]: " DB_HOST
    DB_HOST="${DB_HOST:-localhost}"

    read -rp "Enter Postgres port [5434]: " DB_PORT
    DB_PORT="${DB_PORT:-5434}"

    echo "Database credentials:"
    echo " - User: $DB_USER"
    echo " - Password: $DB_PASSWORD"
    echo " - Host: $DB_HOST"
    echo " - Port: $DB_PORT"
    echo " - Database: $PROJECT_NAME"
}

# Generate .env files
generate_env_files() {
    echo "=== Generating .env files ==="

    # Template with placeholders
    sed "s/{{DB_USER}}/user/g; s/{{DB_PASSWORD}}/pwd/g; s/{{DB_HOST}}/localhost/g; s/{{DB_PORT}}/5432/g; s/{{PROJECT_NAME}}/db_name/g" \
        "$FULL_TEMPLATES_DIR/.env.template" > "$PROJECT_DIR/.env.template"

    # Actual .env with real credentials
    sed "s/{{DB_USER}}/$DB_USER/g; s/{{DB_PASSWORD}}/$DB_PASSWORD/g; s/{{DB_HOST}}/$DB_HOST/g; s/{{DB_PORT}}/$DB_PORT/g; s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
        "$FULL_TEMPLATES_DIR/.env.template" > "$PROJECT_DIR/.env"
}

# Docker setup
setup_docker() {
    read -rp "Run Postgres in Docker? [Y/n]: " choice
    case "${choice:-Y}" in
        [nN])
            echo "Skipping Docker setup"
            echo "========================================================================="
            echo "Не забудьте создать БД '$PROJECT_NAME' вручную на вашем Postgres сервере."
            echo "Если БД с таким именем не будет, то Alembic не сможет создать таблицы"
            echo "========================================================================="
            read -rp "Для продолжения нажмите 'Enter'"
            return
            ;;
        *)
            echo "=== Setting up Docker ==="
            sed "s/{{PROJECT_NAME}}/$PROJECT_NAME/g; s/{{DB_USER}}/$DB_USER/g; s/{{DB_PASSWORD}}/$DB_PASSWORD/g; s/{{DB_PORT}}/$DB_PORT/g" \
                "$FULL_TEMPLATES_DIR/docker-compose.yml.template" > "$PROJECT_DIR/docker-compose.yml"

            (cd "$PROJECT_DIR" && docker compose up -d pg)

            echo "Database connection info:"
            echo " - Host: localhost"
            echo " - Port: $DB_PORT"
            echo " - Database: $PROJECT_NAME"
            echo " - User: $DB_USER"
            echo " - Password: $DB_PASSWORD"
            ;;
    esac
}

# Alembic initialization
setup_alembic() {
    echo "=== Initializing Alembic ==="

    # Initialize alembic in project directory
    (cd "$PROJECT_DIR" && uv run alembic init -t async alembic)

    # Backup original files
    cp "$PROJECT_DIR/alembic.ini" "$PROJECT_DIR/alembic.ini.bak"
    cp "$PROJECT_DIR/alembic/env.py" "$PROJECT_DIR/alembic/env.py.bak"

    # Apply our templates
    cp "$FULL_TEMPLATES_DIR/alembic.ini" "$PROJECT_DIR/"
    cp -R "$FULL_TEMPLATES_DIR/alembic" "$PROJECT_DIR/"

    # Generate and apply migrations
    (cd "$PROJECT_DIR" && uv run alembic revision --autogenerate -m "init")
    (cd "$PROJECT_DIR" && uv run alembic upgrade head)
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
setup_database_credentials
generate_env_files
setup_docker

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
#LOG_FILE_MAX_SIZE=$((10 * 1024 * 1024))  # 10 MB
#LOG_FILE_BACKUP_COUNT=5
