from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import item as items_crud
from models import db_helper
from schemas.item import ItemRead, ItemCreate

router = APIRouter()

@router.get("", response_model=list[ItemRead])
async def get_items(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    # session: AsyncSession = Depends(db_helper.session_getter),
    item = await items_crud.get_all_item(session=session)
    return item

@router.post("", response_model=ItemRead)
async def create_item(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                    item_create: ItemCreate):
    item = await items_crud.create_item(session=session, item=item_create)
    return item

