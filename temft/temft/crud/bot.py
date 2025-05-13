from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from models import Bot
from schemas.bot import BotCreate


async def get_all_bot(session: AsyncSession) -> Sequence[Bot]:
    stmt = select(Bot).order_by(Bot.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_bot(session: AsyncSession, bot: BotCreate) -> Bot:
    try:
        bot = Bot(**bot.model_dump())
        session.add(bot)
        await session.commit()
        await session.refresh(bot)
        return bot
    except IntegrityError as e:
        await session.rollback()
        if "unique constraint" in str(e).lower():
        # if "uq_items_name" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                # detail="Item violates unique constraint"
                detail=f"Item with name '{bot.name}' already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error"
        )

