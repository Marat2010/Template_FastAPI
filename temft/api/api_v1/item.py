from datetime import datetime
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import item as items_crud
from .dependencies import item_by_id
from models import db_helper
from schemas.item import ItemRead, ItemCreate, ItemUpdate, ItemPatch

router = APIRouter()


@router.get("", response_model=list[ItemRead])
async def get_items(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    # session: AsyncSession = Depends(db_helper.session_getter),
    item = await items_crud.get_all_item(session=session)
    return item


@router.get("/{item_id}/",response_model=ItemRead)
async def get_item(
    item: ItemRead = Depends(item_by_id),
):
    return item
    
    
@router.post("", response_model=ItemRead)
async def create_item(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                    item_create: ItemCreate):
    item = await items_crud.create_item(session=session, item=item_create)
    return item


@router.put("/{item_id}/")
async def update_item(
    item_update: ItemUpdate,
    item: ItemRead = Depends(item_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await items_crud.update_item(
        session=session,
        item=item,
        item_update=item_update,
    )


@router.patch("/{item_id}/")
async def update_item_partial(
    item_update: ItemPatch,
    item: ItemRead = Depends(item_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await items_crud.update_item(
        session=session,
        item=item,
        item_update=item_update,
        partial=True,
    )


@router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item: ItemRead = Depends(item_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await items_crud.delete_item(session=session, item=item)


