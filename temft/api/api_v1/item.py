import json
from datetime import datetime
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, status, HTTPException, Query
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
    return await items_crud.create_item(session=session, item=item_create)


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


@router.get("/filter", response_model=list[ItemRead])
async def filter_items(
        name: str | None = Query(None),
        description: str | None = Query(None),
        is_active: bool | None = Query(None),
        created_at_gt: datetime | None = Query(None, description='Пример: "2025-05-24" или "2025-05-24 09:03:00"'),
        # created_at_gt: datetime | None = Query(None),
        created_at_lt: datetime | None = Query(None),
        # updated_at_gt: datetime | None = Query(None),
        # updated_at_lt: datetime | None = Query(None),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    filters = {}
    if name is not None:
        filters['name'] = name
    if description is not None:
        filters['description'] = description
    if is_active is not None:
        filters['is_active'] = is_active

    time_filters = {}
    if created_at_gt:
        time_filters['created_at__gt'] = created_at_gt
    if created_at_lt:
        time_filters['created_at__lt'] = created_at_lt

    items = await items_crud.get_items_by_filters(
        session=session,
        filters=filters,
        time_filters=time_filters
    )
    return items


# ==============================
# ==============================
    # item = await items_crud.create_item(session=session, item=item_create)
# ==============================
    # if updated_at_gt:
    #     time_filters['updated_at__gt'] = updated_at_gt
    # if updated_at_lt:
    #     time_filters['updated_at__lt'] = updated_at_lt
# ==============================
# created_at_gt: datetime | None = Query(None, description="Filter for created_at greater than"),
# created_at_lt: datetime | None = Query(None, description="Filter for created_at less than"),
# updated_at_gt: datetime | None = Query(None, description="Filter for updated_at greater than"),
# updated_at_lt: datetime | None = Query(None, description="Filter for updated_at less than"),
# ==============================
    # if created_at_gt is not None:
    #     time_filters['created_at__gt'] = created_at_gt
    # if created_at_lt is not None:
    #     time_filters['created_at__lt'] = created_at_lt
    # if updated_at_gt is not None:
    #     time_filters['updated_at__gt'] = updated_at_gt
    # if updated_at_lt is not None:
    #     time_filters['updated_at__lt'] = updated_at_lt

# ==============================
# @router.get("/filter", response_model=list[ItemRead])
# async def filter_items(
#     name: str | None = Query(None),
#     description: str | None = Query(None),
#     is_active: bool | None = Query(None),
#     session: AsyncSession = Depends(db_helper.session_getter)
# ):
#     filters = {}
#     if name is not None:
#         filters['name'] = name
#     if description is not None:
#         filters['description'] = description
#     if is_active is not None:
#         filters['is_active'] = is_active
#
#     items = await items_crud.get_items_by_filters(session=session, filters=filters)
#     return items

