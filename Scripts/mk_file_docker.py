import sys

# Проверяем, передан ли аргумент
if len(sys.argv) != 4:
    print(f"Использование: python mk_file_docker.py <PROJECT_NAME> <USER_BD> <PASSWD_BD>")
    sys.exit(1)

PROJECT_NAME = sys.argv[1]  # Получаем значение PROJECT_NAME из аргумента командной строки
USER_BD = sys.argv[2]  # Получаем значение PROJECT_NAME из аргумента командной строки
PASSWD_BD = sys.argv[3]  # Получаем значение PROJECT_NAME из аргумента командной строки

content = f"""services:

  pg:
    image: postgres:17.0-alpine
    environment:
      POSTGRES_DB: {PROJECT_NAME}
      POSTGRES_USER: {USER_BD}
      POSTGRES_PASSWORD: {PASSWD_BD}
    ports:
      - "5434:5432"

  adminer:
    image: adminer
    ports:
      - "8085:8080"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.org
      PGADMIN_DEFAULT_PASSWORD: admin
      PGADMIN_CONFIG_SERVER_MODE: 'False'
    ports:
      - "5055:80"
"""


# Запись в файл
with open(f"./docker-compose.yml", "w") as file:
    file.write(content)

print(f"Файл ./docker-compose.yml успешно создан.")


