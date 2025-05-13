content = """__all__ = (
    "camel_case_to_snake_case",
)
from .case_converter import camel_case_to_snake_case

"""

# Запись в файл
with open(f"utils/__init__.py", "w") as file:
    file.write(content)

print(f"Файл utils/__init__.py успешно создан.")
