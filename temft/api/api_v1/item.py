from datetime import datetime

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from crud import item as items_crud
from .dependencies import item_by_id
from models import db_helper
from schemas.item import ItemRead, ItemCreate, ItemUpdate, ItemPatch

router = APIRouter()


@router.get("", response_model=list[ItemRead])
async def get_items(session: AsyncSession = Depends(db_helper.session_getter)):
    item = await items_crud.get_all_item(session=session)
    return item


@router.get("/{item_id}/", response_model=ItemRead)
async def get_item(item: ItemRead = Depends(item_by_id)):
    return item


@router.post("", response_model=ItemRead)
async def create_item(item_create: ItemCreate,
                      session: AsyncSession = Depends(db_helper.session_getter)):
    return await items_crud.create_item(item=item_create, session=session)


@router.put("/{item_id}/")
async def update_item(item_update: ItemUpdate,
                      item: ItemRead = Depends(item_by_id),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    return await items_crud.update_item(
        item_update=item_update,
        item=item,
        session=session)


@router.patch("/{item_id}/")
async def update_item_partial(item_update: ItemPatch,
                              item: ItemRead = Depends(item_by_id),
                              session: AsyncSession = Depends(db_helper.session_getter)):
    return await items_crud.update_item(
        item_update=item_update,
        item=item,
        session=session,
        partial=True)


@router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item: ItemRead = Depends(item_by_id),
                      session: AsyncSession = Depends(db_helper.session_getter)) -> None:
    await items_crud.delete_item( item=item, session=session)


@router.get("/filter", response_model=list[ItemRead])
async def filter_items(
        name: str | None = Query(None),
        description: str | None = Query(None),
        is_active: bool | None = Query(None),
        created_at_gt: datetime | None = Query(None, description='Пример: "2025-05-24" или "2025-05-24 09:03:00"'),
        created_at_lt: datetime | None = Query(None),
        session: AsyncSession = Depends(db_helper.session_getter)):
    filters = {}
    if name:
        filters['name'] = name
    if description:
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


# ==========================================================
# ==========================================================
    # session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
# ==========================================================
    # if updated_at_gt:
    #     time_filters['updated_at__gt'] = updated_at_gt
    # if updated_at_lt:
    #     time_filters['updated_at__lt'] = updated_at_lt
# ==========================================================
# updated_at_gt: datetime | None = Query(None, description="Filter for updated_at greater than"),
# updated_at_lt: datetime | None = Query(None, description="Filter for updated_at less than"),
# ==========================================================
    # if name is not None:

