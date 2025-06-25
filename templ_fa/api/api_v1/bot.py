# template_FA/api/api_v1/bot.py.template
from datetime import datetime

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from crud import bot as bot_crud
from .dependencies import bot_by_id
from models import db_helper
from schemas.bot import BotRead, BotCreate, BotUpdate, BotPatch

router = APIRouter()


@router.get("", response_model=list[BotRead])
async def get_bots(session: AsyncSession = Depends(db_helper.session_getter)):
    bot = await bot_crud.get_all_bot(session=session)
    return bot


@router.get("/{bot_id}/", response_model=BotRead)
async def get_bot(bot: BotRead = Depends(bot_by_id)):
    return bot
    
    
@router.post("", response_model=BotRead)
async def create_bot(bot_create: BotCreate,
                      session: AsyncSession = Depends(db_helper.session_getter)):
    return await bot_crud.create_bot(bot=bot_create, session=session)


@router.put("/{bot_id}/")
async def update_bot(bot_update: BotUpdate,
                      bot: BotRead = Depends(bot_by_id),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    return await bot_crud.update_bot(
        bot_update=bot_update,
        bot=bot,
        session=session)


@router.patch("/{bot_id}/")
async def update_bot_partial(bot_update: BotPatch,
                              bot: BotRead = Depends(bot_by_id),
                              session: AsyncSession = Depends(db_helper.session_getter)):
    return await bot_crud.update_bot(
        bot_update=bot_update,        
        bot=bot,
        session=session,
        partial=True)


@router.delete("/{bot_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot(bot: BotRead = Depends(bot_by_id),
                      session: AsyncSession = Depends(db_helper.session_getter)) -> None:
    await bot_crud.delete_bot(bot=bot, session=session)


@router.get("/filter", response_model=list[BotRead])
async def filter_bots(
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

    bot = await bot_crud.get_bots_by_filters(
        session=session,
        filters=filters,
        time_filters=time_filters
    )
    return bot


# ==========================================================
    # session: Annotated[AsyncSession, Depends(db_helper.session_getter)]

