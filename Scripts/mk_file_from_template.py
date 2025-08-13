# Файл mk_file_from_template.py

import sys
import re
from pathlib import Path

import logging
from datetime import datetime
import os  # Для автоматического создания папки Logs

# Создаем папку для логов, если её нет
os.makedirs("Logs", exist_ok=True)

# Формируем имя файла с датой (например: "Logs/template_gen_debug_2024-01-31.log")
log_filename = f"Logs/template_gen_{datetime.now().strftime('%Y-%m-%d')}.log"

# Настройка логирования (дозапись в файл)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',  # Убираем миллисекунды
    filename=log_filename,
    filemode='a'  # 'a' = append (добавление), 'w' = write (перезапись)
)

# Добавляем вывод в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'  # Убираем миллисекунды и здесь
    )
)
logging.getLogger().addHandler(console_handler)


def snake_to_camel(snake_str: str) -> str:
    return ''.join(word.title() for word in snake_str.split('_'))


def normalize_entity_name(name: str) -> tuple[str, str]:
    snake = re.sub(r'[^a-zA-Z0-9]+', '_', name).lower().strip('_')
    snake = re.sub(r'_+', '_', snake)
    return snake, ''.join(word.title() for word in snake.split('_'))


def process_template(
        template_path: Path,
        output_path: Path,
        replacements: dict  # Словарь с заменами: {"{{KEY}}": "value"}
) -> None:
    try:
        content = template_path.read_text(encoding='utf-8')
        for key, value in replacements.items():
            content = content.replace(key, value)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')
        logging.info(f"[OK] Файл {output_path} создан!")
    except Exception as e:
        logging.error(f"\n===!!!!! Ошибка при обработке {template_path}: {e}===\n")


def main():
    # logging.info(f"Запуск с аргументами: {sys.argv}")

    if len(sys.argv) < 3:
        logging.error(
            "Использование: python mk_file_from_template.py <ENTITY_NAME> <TEMPLATE_RELATIVE_PATH>"
            " [PROJECT_DIR] [TEMPLATES_DIR] [PROJECT_NAME] [PYTHON_VERSION] [DB_USER] [DB_PASSWORD]")
        sys.exit(1)

    # Парсим аргументы
    args = {
        'entity_name': sys.argv[1],
        'template_rel_path': sys.argv[2],
        'project_dir': sys.argv[3] if len(sys.argv) > 3 else ".",
        'templates_dir': sys.argv[4] if len(sys.argv) > 4 else "template_FA",
        'project_name': sys.argv[5] if len(sys.argv) > 5 else "templ_fa",
        'python_version': sys.argv[6] if len(sys.argv) > 6 else "3.10",
        'db_user': sys.argv[7] if len(sys.argv) > 7 else "marat",
        'db_password': sys.argv[8] if len(sys.argv) > 8 else "1"
    }

    # Нормализуем имя сущности
    entity_name, entity_name_camel = normalize_entity_name(args['entity_name'])
    if not entity_name:
        logging.error(f"!!!!!  Недопустимое имя сущности: '{args['entity_name']}'")
        sys.exit(1)

    # Формируем замены
    replacements = {
        '{{ENTITY_NAME}}': entity_name,
        '{{ENTITY_NAME_CAMEL}}': entity_name_camel,
        '{{PROJECT_NAME}}': args['project_name'],
        '{{PYTHON_VERSION}}': args['python_version'],
        '{{DB_USER}}': args['db_user'],
        '{{DB_PASSWORD}}': args['db_password']
    }

    # Обрабатываем шаблон
    template_path = Path(args['templates_dir']) / args['template_rel_path']
    output_rel_path = args['template_rel_path'].replace('.template', '').replace('{{ENTITY_NAME}}', entity_name)
    output_path = Path(args['project_dir']) / output_rel_path

    if not template_path.exists():
        logging.error(f"!!!!! Шаблон {template_path} не найден!")
        sys.exit(1)

    process_template(template_path, output_path, replacements)


if __name__ == "__main__":
    main()


# =====================================
# =====================================

# # Включим логирование в файл
# import logging
#
# logging.basicConfig(
#     level=logging.INFO,
#     format='[%(asctime)s] [%(levelname)s] %(message)s',
#     filename='Logs/template_gen_debug.log',
#     filemode='w'
# )
# # Пример лога
# logging.info("Этот лог добавится в файл, а не перезапишет его!")