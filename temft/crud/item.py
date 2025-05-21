from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

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
    try:
        item = Item(**item.model_dump())
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item
    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e).lower():
        # if "uq_items_name" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                # detail="Item violates unique constraint"
                detail=f"Item with name '{item.name}' already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error"
        )


async def update_item(
    session: AsyncSession,
    item: Item,
    item_update: ItemUpdate | ItemPatch,
    partial: bool = False,
) -> Item:
    for name, value in item_update.model_dump(exclude_unset=partial).items():
        setattr(item, name, value)
    await session.commit()
    return item


async def delete_item(session: AsyncSession, item: Item,) -> None:
    await session.delete(item)
    await session.commit()
    
