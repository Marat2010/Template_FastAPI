from typing import Sequence

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from api.api_v1.exceptions import ItemNameConflict
from models import Item
from schemas.item import ItemCreate, ItemUpdate, ItemPatch 


async def get_all_item(session: AsyncSession) -> Sequence[Item]:
    stmt = select(Item).order_by(Item.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_item(session: AsyncSession, item_id: int) -> Item | None:
    return await session.get(Item, item_id)


async def get_items_by_field(session: AsyncSession, field_name: str, value: str) -> Sequence[Item]:
    # Получаем атрибут модели по имени поля
    field = getattr(Item, field_name)
    stmt = select(Item).where(field == value)
    result = await session.scalars(stmt)
    return result.all()


async def create_item(session: AsyncSession, item: ItemCreate) -> Item:
    # Проверка перед созданием
    if await session.scalar(select(Item).where(Item.name == item.name)):
        raise ItemNameConflict()

    db_item = Item(**item.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


async def update_item(
    session: AsyncSession,
    item: Item,
    item_update: ItemUpdate | ItemPatch,
    partial: bool = False,
) -> Item:
    # for name, value in item_update.model_dump(exclude_unset=partial).items():
    #     setattr(item, name, value)

    update_data = item_update.model_dump(exclude_unset=partial)

    if "name" in update_data:
        if await session.scalar(
            select(Item)
            .where(Item.name == update_data["name"])
            .where(Item.id != item.id)
        ):
            raise ItemNameConflict()

    # if 'name' in update_data:
    #     await check_name_unique(session, update_data['name'], exclude_item_id=item.id)

    for name, value in update_data.items():
        setattr(item, name, value)

    await session.commit()
    return item


async def delete_item(session: AsyncSession, item: Item,) -> None:
    await session.delete(item)
    await session.commit()


async def get_items_by_filters(
        session: AsyncSession,
        filters: dict,
        time_filters: dict | None = None
) -> Sequence[Item]:
    stmt = select(Item)

    # Применяем обычные фильтры (равенство)
    for field_name, value in filters.items():
        field = getattr(Item, field_name)
        stmt = stmt.where(field == value)

    # Применяем временные фильтры (больше/меньше)
    if time_filters:
        for filter_key, value in time_filters.items():
            field_name, operator = filter_key.split('__')
            field = getattr(Item, field_name)

            if operator == 'gt':
                stmt = stmt.where(field > value)
            elif operator == 'lt':
                stmt = stmt.where(field < value)

    result = await session.scalars(stmt)
    return result.all()


# ====================================
# ====================================

# async def create_item(session: AsyncSession, item: ItemCreate) -> Item:
#     try:
#         item = Item(**item.model_dump())
#         session.add(item)
#         await session.commit()
#         await session.refresh(item)
#         return item
#     except IntegrityError as e:
#         await session.rollback()
#         if "unique constraint" in str(e).lower():
#         # if "uq_items_name" in str(e):
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 # detail="Item violates unique constraint"
#                 detail=f"Item with name '{item.name}' already exists"
#             )
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Database integrity error"
#         )

# ====================================
# async def check_name_unique(
#     session: AsyncSession,
#     name: str,
#     exclude_item_id: int | None = None
# ) -> None:
#     """Проверяет, существует ли item с таким name (исключая текущий item при обновлении)."""
#     filters = {'name': name}
#     if exclude_item_id:
#         existing_items = await get_items_by_filters(session, filters)
#         # Исключаем текущий item из проверки при обновлении
#         existing_items = [item for item in existing_items if item.id != exclude_item_id]
#         if existing_items:
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail=f"Item with this name: '{name}' already exists"
#             )
#     else:
#         # Для создания - просто проверяем существование
#         if await get_items_by_filters(session, filters):
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail=f"Item with this name: '{name}' already exists"
#             )
# ====================================
    # await check_name_unique(session, item.name)
# ====================================
# for filter_key, value in time_filters.items():
#     if '__' in filter_key:  # Для формата field__operator
#         field_name, operator = filter_key.split('__')
#         field = getattr(Item, field_name)
#
#         if operator == 'gt':
#             stmt = stmt.where(and_(field > value))
#         elif operator == 'lt':
#             stmt = stmt.where(and_(field < value))
#         # Можно добавить другие операторы
#     else:  # Для формата {"field": {"operator": value}}
#         field = getattr(Item, filter_key)
#         for op, val in value.items():
#             if op == 'gt':
#                 stmt = stmt.where(and_(field > val))
#             elif op == 'lt':
#                 stmt = stmt.where(and_(field < val))
# ====================================
    # if time_filters:
    #     for filter_key, value in time_filters.items():
    #         field_name, operator = filter_key.split('__')
    #         field = getattr(Item, field_name)
    #
    #         if operator == 'gt':
    #             stmt = stmt.where(field > value)
    #         elif operator == 'lt':
    #             stmt = stmt.where(field < value)
# ====================================
# async def get_items_by_filters(session: AsyncSession, filters: dict) -> Sequence[Item]:
#     stmt = select(Item)
#
#     for field_name, value in filters.items():
#         field = getattr(Item, field_name)
#         stmt = stmt.where(field == value)
#
#     result = await session.scalars(stmt)
#     return result.all()
