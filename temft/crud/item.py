from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.exceptions import ItemNameConflict
from models import Item
from schemas.item import ItemCreate, ItemUpdate, ItemPatch 

from utils.filters import apply_filters


async def get_all_item(session: AsyncSession) -> Sequence[Item]:
    stmt = select(Item).order_by(Item.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_item(session: AsyncSession, item_id: int) -> Item | None:
    return await session.get(Item, item_id)


async def is_name_exists(session: AsyncSession,
                         name: str,
                         exclude_item_id: int | None = None) -> bool:
    query = select(Item).where(Item.name == name)
    if exclude_item_id is not None:
        query = query.where(Item.id != exclude_item_id)
    return bool(await session.scalar(query))


async def create_item(item: ItemCreate, session: AsyncSession) -> Item:
    # Проверка перед созданием
    if await is_name_exists(session, item.name):
        raise ItemNameConflict()

    db_item = Item(**item.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


async def update_item(item_update: ItemUpdate | ItemPatch,
                      item: Item,
                      session: AsyncSession,
                      partial: bool = False, ) -> Item:

    update_data = item_update.model_dump(exclude_unset=partial)

    if "name" in update_data and await is_name_exists(session, update_data["name"], item.id):
        raise ItemNameConflict()

    for name, value in update_data.items():
        setattr(item, name, value)

    await session.commit()
    return item


async def delete_item(item: Item, session: AsyncSession) -> None:
    await session.delete(item)
    await session.commit()


async def get_items_by_filters(
    session: AsyncSession,
    filters: dict | None = None,
    time_filters: dict | None = None
) -> Sequence[Item]:
    stmt = apply_filters(Item, filters, time_filters)
    result = await session.scalars(stmt)
    return result.all()


# =========================================
# =========================================
    # return await session.scalar(query) is not None
# =========================================
    # if await session.scalar(select(Item).where(Item.name == item.name)):
    #     raise ItemNameConflict()

    # if "name" in update_data:
    #     if await session.scalar(
    #         select(Item)
    #         .where(Item.name == update_data["name"])
    #         .where(Item.id != item.id)
    #     ):
    #         raise ItemNameConflict()
# =========================================
# async def get_items_by_filters(
#         session: AsyncSession,
#         filters: dict,
#         time_filters: dict | None = None
# ) -> Sequence[Item]:
#     stmt = select(Item)
#
#     # Применяем обычные фильтры (равенство)
#     for field_name, value in filters.items():
#         field = getattr(Item, field_name)
#         stmt = stmt.where(field == value)
#
#     # Применяем временные фильтры (больше/меньше)
#     if time_filters:
#         for filter_key, value in time_filters.items():
#             field_name, operator = filter_key.split('__')
#             field = getattr(Item, field_name)
#
#             if operator == 'gt':
#                 stmt = stmt.where(field > value)
#             elif operator == 'lt':
#                 stmt = stmt.where(field < value)
#
#     result = await session.scalars(stmt)
#     return result.all()
# =========================================
# async def delete_item(session: AsyncSession, item: Item,) -> None:
# =========================================

