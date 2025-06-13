# utils/filters.py
from sqlalchemy import inspect, String, Text, Unicode
from sqlalchemy.sql import select, Select
from typing import Type, Any


def apply_filters(model: Type[Any],
                  filters: dict | None = None,
                  time_filters: dict | None = None) -> Select:
    """
    Создает и возвращает SQL-запрос с примененными фильтрами.
    Args:
        model: SQLAlchemy модель
        filters: Обычные фильтры (поле=значение)
        time_filters: Временные фильтры (поле__gt/поле__lt)
    """
    stmt = select(model)

    if filters:
        for field_name, value in filters.items():
            field = getattr(model, field_name)

            # Получаем информацию о типе поля
            column_type = inspect(model).columns[field_name].type

            # Если поле строковое — используем ilike, иначе обычное сравнение
            if isinstance(column_type, (String, Text, Unicode)):
                stmt = stmt.where(field.ilike(f"%{value}%"))
            else:
                stmt = stmt.where(field == value)

    if time_filters:
        for filter_key, value in time_filters.items():
            field_name, operator = filter_key.split('__')
            field = getattr(model, field_name)

            if operator == 'gt':
                stmt = stmt.where(field > value)
            elif operator == 'lt':
                stmt = stmt.where(field < value)

    return stmt

