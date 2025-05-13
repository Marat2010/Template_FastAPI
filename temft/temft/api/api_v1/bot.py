from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import bot as bots_crud
from models import db_helper
from schemas.bot import BotRead, BotCreate

router = APIRouter()

@router.get("", response_model=list[BotRead])
async def get_bots(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    # session: AsyncSession = Depends(db_helper.session_getter),
    bot = await bots_crud.get_all_bot(session=session)
    return bot

@router.post("", response_model=BotRead)
async def create_bot(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                    bot_create: BotCreate):
    bot = await bots_crud.create_bot(session=session, bot=bot_create)
    return bot

