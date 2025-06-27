import sys
import re
from pathlib import Path


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
        print(f"[OK] Файл {output_path} создан!")
    except Exception as e:
        print(f"\n===[ERROR] Ошибка при обработке {template_path}: {e}===\n")


def main():
    if len(sys.argv) < 3:
        print(
            "Использование: python mk_file_from_template.py <ENTITY_NAME> <TEMPLATE_RELATIVE_PATH> [PROJECT_DIR] [TEMPLATES_DIR] [PROJECT_NAME] [PYTHON_VERSION]")
        sys.exit(1)

    # Парсим аргументы
    args = {
        'entity_name': sys.argv[1],
        'template_rel_path': sys.argv[2],
        'project_dir': sys.argv[3] if len(sys.argv) > 3 else ".",
        'templates_dir': sys.argv[4] if len(sys.argv) > 4 else "template_FA",
        'project_name': sys.argv[5] if len(sys.argv) > 5 else "templ_fa",
        'python_version': sys.argv[6] if len(sys.argv) > 6 else "3.10"
    }

    # Нормализуем имя сущности
    entity_name, entity_name_camel = normalize_entity_name(args['entity_name'])
    if not entity_name:
        print(f"[ERROR] Недопустимое имя сущности: '{args['entity_name']}'")
        sys.exit(1)

    # Формируем замены
    replacements = {
        '{{ENTITY_NAME}}': entity_name,
        '{{ENTITY_NAME_CAMEL}}': entity_name_camel,
        '{{PROJECT_NAME}}': args['project_name'],
        '{{PYTHON_VERSION}}': args['python_version']
    }

    # Обрабатываем шаблон
    template_path = Path(args['templates_dir']) / args['template_rel_path']
    output_rel_path = args['template_rel_path'].replace('.template', '').replace('{{ENTITY_NAME}}', entity_name)
    output_path = Path(args['project_dir']) / output_rel_path

    if not template_path.exists():
        print(f"[ERROR] Шаблон {template_path} не найден!")
        sys.exit(1)

    process_template(template_path, output_path, replacements)


if __name__ == "__main__":
    main()
