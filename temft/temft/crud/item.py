from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models import Item
from schemas.item import ItemCreate


async def get_all_item(session: AsyncSession) -> Sequence[Item]:
    stmt = select(Item).order_by(Item.id)
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

