#!/bin/bash
set -e
#set -x  # Добавляем для отладки (покажет какие команды выполняются)

# Файл Generate_Project_FastAPI.sh

# --- Constants ---
DEFAULT_PROJECT_NAME="proj_fa"
DEFAULT_ENTITY_NAME="book"
TEMPLATES_DIR="template_FA"
SCRIPTS_DIR="Scripts"

# --- Логирование ---
LOG_DIR="Logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/generate_project_$(date '+%Y%m%d_%H%M%S').log"

#log() {
#    local message="$1"
#    local timestamp
#    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
#    echo "${timestamp} - ${message}" | tee -a "$LOG_FILE"
#}

log() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[${timestamp}] [INFO] ${message}" | tee -a "$LOG_FILE"
}

#log_error() {
#    local message="$1"
#    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
#    echo -e "[${timestamp}] [\e[31mERROR\e[0m] ${message}" | tee -a "$LOG_FILE" >&2
#}

add_error_tag() {
    sed 's/\[ERROR\]/\x1b[31m&\x1b[0m/g'
}

log_error() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_entry="[${timestamp}] [ERROR] ${message}"

    # В консоль - с цветом
    echo -e "$log_entry" | add_error_tag >&2
    # В файл - без цвета
    echo "$log_entry" >> "$LOG_FILE"
}

# Первая запись в лог
log "Скрипт запущен"

run_cmd() {
    if "$@"; then
        log "Команда выполнена: $*"
        return 0
    else
        local status=$?
        log_error "Ошибка выполнения: $* (статус: $status)"
        return $status
    fi
}

# --- Functions ---

# Проверка зависимостей
check_dependencies() {
    local deps=("python3" "docker" "psql" "pg_isready" "uv")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            log_error "Error: Required tool '$dep' is not installed"
            exit 1
        fi
    done
}

# Validate entity name (letters, numbers, underscores, hyphens)
validate_entity_name() {
    if [[ ! "$1" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        log_error "Error: Entity name can only contain letters, numbers, hyphens and underscores"
        exit 1
    fi
}

# Validate project name
validate_project_name() {
    if [[ ! "$1" =~ ^[a-zA-Z][a-zA-Z0-9_-]{1,63}$ ]]; then
        log_error "Error: Invalid project name. Must start with letter, 2-64 chars, only a-z, 0-9, _-"
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
                log "Используем существующий Postgres сервер"
                DB_TYPE=1  # Явно сохраняем выбор в переменную
                return 0
                ;;
            2)
                log "Создаем Postgres сервер в Docker"
                DB_TYPE=2  # Явно сохраняем выбор в переменную
                return 0
                ;;
            *)
                log "Неверный выбор подключения к БД, попробуйте снова"
                ;;
        esac
    done
}

# Database connection setup
setup_database_connection() {
    select_database_type

    # Common credentials
    echo
    read -rp "Введите имя пользователя Postgres [${USER}]: " DB_USER
    DB_USER="${DB_USER:-$USER}"

    read -rp "Введите пароль пользователя [1]: " DB_PASSWORD
    DB_PASSWORD="${DB_PASSWORD:-1}"

    read -rp "Введите имя базы данных [${PROJECT_NAME}]: " DB_NAME
    DB_NAME="${DB_NAME:-$PROJECT_NAME}"

    if [ $DB_TYPE -eq 1 ]; then
        # Existing server
        read -rp "Введите хост Postgres [localhost]: " DB_HOST
        DB_HOST="${DB_HOST:-localhost}"

        read -rp "Введите порт Postgres [5432]: " DB_PORT
        DB_PORT="${DB_PORT:-5432}"

        log "Проверка подключения к серверу..."
        if ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; then
            log_error "Ошибка: Не удалось подключиться к Postgres серверу!"
            exit 1
        fi

        log "Проверка существования базы данных..."
        if ! PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
            log "База данных '$DB_NAME' не существует. Создать её? [Y/n]"
            read -r create_db
            if [[ "$create_db" =~ ^[Nn]$ ]]; then
                log "Необходимо создать БД вручную перед продолжением"
                exit 1
            else
                PGPASSWORD="$DB_PASSWORD" createdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME"
            fi
        fi
    else
        # Docker setup
        DB_HOST="localhost"
        read -rp "Введите порт для Docker Postgres [5434]: " DB_PORT
        DB_PORT="${DB_PORT:-5434}"

        # Убедимся, что DB_NAME не пустое
        DB_NAME="${DB_NAME:-$PROJECT_NAME}"

        # Генерация docker-compose.yml
        sed -e "s/{{DB_USER}}/$DB_USER/g" \
            -e "s/{{DB_PASSWORD}}/$DB_PASSWORD/g" \
            -e "s/{{DB_PORT}}/$DB_PORT/g" \
            -e "s/{{DB_NAME}}/$DB_NAME/g" \
            -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
            "$FULL_TEMPLATES_DIR/docker-compose.yml.template" > "$PROJECT_DIR/docker-compose.yml"

        # Проверка существования контейнера
        if docker ps -a --format '{{.Names}}' | grep -q "${PROJECT_NAME}_pg"; then
            read -rp "Docker контейнер с именем '${PROJECT_NAME}_pg' уже существует. Пересоздать? [y/N] " recreate
            if [[ "$recreate" =~ ^[Yy]$ ]]; then
#                docker rm -f "${PROJECT_NAME}_pg"
                run_cmd docker rm -f -v "${PROJECT_NAME}_pg"
                run_cmd docker volume rm "${PROJECT_NAME}_pg_data"
                run_cmd docker network rm "${PROJECT_NAME}_default"
                log "Удалили существующий контейнер с именем '${PROJECT_NAME}_pg'"
            else
                log "Используем существующий контейнер с именем '${PROJECT_NAME}_pg'"
                return
            fi
        fi

        # Start container
        log "Запускаем Docker контейнер с именем '${PROJECT_NAME}_pg'..."
        #        (cd "$PROJECT_DIR" && run_cmd docker compose up -d pg)
        if (cd "$PROJECT_DIR" && docker compose up -d pg); then
          log "Docker контейнер успешно запущен"
        else
          log_error "Ошибка запуска контейнера PostgreSQL"
          exit 1
        fi

        # Wait for DB to be ready
        log "Ожидаем инициализации Postgres (2 сек)..."
        sleep 2
    fi

    log "===================================================================="
    log " Настройки подключения к PostgreSQL:"
    log "--------------------------------------------------------------------"
    log " Хост:        $DB_HOST"
    log " Порт:        $DB_PORT"
    log " База данных: $DB_NAME"
    log " Пользователь: $DB_USER"
    log " Пароль:      $DB_PASSWORD"
    [ $DB_TYPE -eq 2 ] && log " (Docker контейнер)"
    log "===================================================================="
}

# Generate .env files (updated)
generate_env_files() {
    log "=== Создание файлов .env ==="

    # Template with placeholders
    sed "s/{{DB_USER}}/user/g; s/{{DB_PASSWORD}}/pwd/g; s/{{DB_HOST}}/localhost/g; s/{{DB_PORT}}/5432/g; s/{{DB_NAME}}/db_name/g" \
        "$FULL_TEMPLATES_DIR/.env.template" > "$PROJECT_DIR/.env.template"

    # Actual .env with real credentials
    sed "s/{{DB_USER}}/$DB_USER/g; s/{{DB_PASSWORD}}/$DB_PASSWORD/g; s/{{DB_HOST}}/$DB_HOST/g; s/{{DB_PORT}}/$DB_PORT/g; s/{{DB_NAME}}/$DB_NAME/g" \
        "$FULL_TEMPLATES_DIR/.env.template" > "$PROJECT_DIR/.env"
}

# Generate project files (Заменили последовательный цикл на параллельный)
generate_files_parallel() {
    local max_jobs=4
    for template in "${TEMPLATES[@]}"; do
        while [ "$(jobs -r | wc -l)" -ge "$max_jobs" ]; do sleep 0.1; done
        python3 "$FULL_SCRIPTS_DIR/mk_file_from_template.py" \
            "$ENTITY_NAME" "$template" "$PROJECT_DIR" "$FULL_TEMPLATES_DIR" \
            "$PROJECT_NAME" "$PYTHON_VERSION" "$DB_USER" "$DB_PASSWORD" &
    done
    wait
}

#generate_files_parallel() {
#    local max_jobs=4
#    local counter=0
#    local total=${#TEMPLATES[@]}
#
#    log "Генерация $total файлов (параллельно, макс $max_jobs процессов)"
#
#    # Временный файл для сбора логов
#    local parallel_log="${PROJECT_DIR}/parallel_gen.log"
#    : > "$parallel_log"
#
#    for template in "${TEMPLATES[@]}"; do
#        ((counter++))
#        while [ "$(jobs -r | wc -l)" -ge "$max_jobs" ]; do sleep 0.1; done
#
#        {
#            local short_name="${template##*/}"
#            local output
#
#            # Явный вызов с перенаправлением вывода
#            output=$(
#                python3 "$FULL_SCRIPTS_DIR/mk_file_from_template.py" \
#                    "$ENTITY_NAME" "$template" \
#                    "$(realpath "$PROJECT_DIR")" \
#                    "$(realpath "$FULL_TEMPLATES_DIR")" \
#                    "$PROJECT_NAME" "$PYTHON_VERSION" \
#                    "$DB_USER" "$DB_PASSWORD" 2>&1
#            )
#
#            # Запись в лог с меткой времени
#            printf "[%s] %s:\n%s\n" \
#                "$(date '+%Y-%m-%d %H:%M:%S')" \
#                "$short_name" \
#                "$output" >> "$parallel_log"
#        } &
#    done
#
#    wait
#
#    # Вывод результатов
#    log "Результаты генерации:"
#    cat "$parallel_log"
#    cat "$parallel_log" >> "$LOG_FILE"
#    rm -f "$parallel_log"
#
#    log "Генерация файлов завершена"
#}


#generate_files_parallel() {
#    local max_jobs=4
#    local counter=0
#    local total=${#TEMPLATES[@]}
#    local error_count=0
#
#    log "Начало генерации $total файлов (параллельно)"
#
#    for template in "${TEMPLATES[@]}"; do
#        ((counter++))
#        while [ "$(jobs -r | wc -l)" -ge "$max_jobs" ]; do sleep 0.1; done
#
#        {
#            local short_name="${template##*/}"
#            local output
#
#            # Явный вызов с полными путями
#            output=$(python3 "$FULL_SCRIPTS_DIR/mk_file_from_template.py" \
#                "$ENTITY_NAME" "$template" \
#                "$(realpath "$PROJECT_DIR")" \
#                "$(realpath "$FULL_TEMPLATES_DIR")" \
#                "$PROJECT_NAME" "$PYTHON_VERSION" \
#                "$DB_USER" "$DB_PASSWORD" 2>&1)
#            local status=$?
#
#            if [ $status -eq 0 ]; then
#                log "[$counter/$total] Успех: $short_name"
#            else
#                log_error "[$counter/$total] Ошибка: $short_name"
#                echo "$output" >&2
#                ((error_count++))
#            fi
#        } &
#    done
#
#    wait
#
#    if [ $error_count -gt 0 ]; then
#        log_error "Завершено с $error_count ошибками"
#        return 1
#    else
#        log "Все файлы успешно сгенерированы"
#        return 0
#    fi
#}

# Alembic initialization
setup_alembic() {
    log "=== Начало инициализации Alembic ==="

    # Жёстко удаляем папку, если существует
    local alembic_dir="$PROJECT_DIR/alembic"
    if [ -d "$alembic_dir" ]; then
        log "Удаляем существующую папку alembic..."
        rm -rf "$alembic_dir"
    fi

    # Initialize alembic in project directory
    (cd "$PROJECT_DIR" && uv run alembic init -t async alembic) || {
        log_error "Ошибка инициализации Alembic"
        return 1
    }

    # Backup original files
    cp "$PROJECT_DIR/alembic.ini" "$PROJECT_DIR/alembic.ini.bak"
    cp "$PROJECT_DIR/alembic/env.py" "$PROJECT_DIR/alembic/env.py.bak"

    # Apply our templates
    cp "$FULL_TEMPLATES_DIR/alembic.ini" "$PROJECT_DIR/"
    cp -R "$FULL_TEMPLATES_DIR/alembic" "$PROJECT_DIR/"

    # Generate and apply migrations
    (cd "$PROJECT_DIR" && uv run alembic revision --autogenerate -m "init")
#    (cd "$PROJECT_DIR" && uv run alembic upgrade head)
    if (cd "$PROJECT_DIR" && uv run alembic upgrade head); then
      log "Миграции применены успешно"
    else
      log_error "Ошибка применения миграций"
      exit 1
    fi

    log "Alembic успешно настроен"
}

# Вывод итогов
show_summary() {
    log "===================================================================="
    log " Проект успешно создан!"
    log "--------------------------------------------------------------------"
    log " Имя проекта:   $PROJECT_NAME"
    log " Основная сущность: $ENTITY_NAME"
    log " Каталог проекта: $(realpath "$PROJECT_DIR")"
    log " Python версия:  $PYTHON_VERSION"
    log
    log " Для запуска:"
    log "   cd $PROJECT_NAME"
#    [ $DB_TYPE -eq 2 ] && log "   docker compose up -d"
    log "   uv run main.py"
    log "===================================================================="
}


#===============================
# --- Main Script ---

# 0. Проверка зависимостей
check_dependencies
log "Проверка зависимостей прошла (OK)"

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
validate_project_name "$PROJECT_NAME"

# 3. Create project directory
PROJECT_DIR="$PROJECT_NAME"
mkdir -p "$PROJECT_DIR" || { log "Failed to create project directory"; exit 1; }
log "Создана папка проекта: $PROJECT_NAME"
log "Основная сущность: $ENTITY_NAME"

# 4. Select Python version
PYTHON_VERSION=$(select_python_version)
log "Выбрана Python версия: $PYTHON_VERSION"

# 5. Set paths
SCRIPT_DIR="$(dirname "$0")"
FULL_TEMPLATES_DIR="$SCRIPT_DIR/$TEMPLATES_DIR"
FULL_SCRIPTS_DIR="$SCRIPT_DIR/$SCRIPTS_DIR"

# 6. Database setup
setup_database_connection
generate_env_files
#log "База данных настроена: host=$DB_HOST, port=$DB_PORT"


# 7. Generate project files
log "=== Generating project files ==="
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
    "sassas"
)

generate_files_parallel

# 8. Initialize Alembic
setup_alembic

# 9. Вывод итогов
show_summary


#=======================================
#=======================================
#        log "Запуск контейнера PostgreSQL..."
#        pushd "$PROJECT_DIR" >/dev/null
#        run_cmd docker compose up -d pg
#        popd >/dev/null

#        (
#            cd "$PROJECT_DIR"
#            source ../Generate_Project_FastAPI.sh  # Перезагружаем переменные
#            run_cmd docker compose up -d pg
#        )
#=======================================
#for template in "${TEMPLATES[@]}"; do
#    python3 "$FULL_SCRIPTS_DIR/mk_file_from_template.py" \
#        "$ENTITY_NAME" \
#        "$template" \
#        "$PROJECT_DIR" \
#        "$FULL_TEMPLATES_DIR" \
#        "$PROJECT_NAME" \
#        "$PYTHON_VERSION" \
#        "$DB_USER" \
#        "$DB_PASSWORD"
#done
#=======================================
#log() {
#    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
#}
#=======================================
#b) Обработка паролей:
  # В функции setup_database_connection
#    read -rsp "Введите пароль пользователя [1]: " DB_PASSWORD
#    DB_PASSWORD="${DB_PASSWORD:-1}"
#    echo
#=======================================
#echo "=== Project setup complete ==="
#echo "Project directory: $PROJECT_DIR"
#=======================================
