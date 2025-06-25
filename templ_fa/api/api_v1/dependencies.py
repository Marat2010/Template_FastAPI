# template_FA/api/api_v1/dependencies.py.template
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper, Bot
from crud import bot as bot_crud


async def bot_by_id(
    bot_id: Annotated[int, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Bot:

    bot = await bot_crud.get_bot(session=session, bot_id=bot_id)
    if bot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot id: {bot_id} not found!")

    return bot

