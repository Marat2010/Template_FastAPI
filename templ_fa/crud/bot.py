from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.exceptions import BotNameConflict
from models import Bot
from schemas.bot import BotCreate, BotUpdate, BotPatch 

from utils.filters import apply_filters


async def get_all_bot(session: AsyncSession) -> Sequence[Bot]:
    stmt = select(Bot).order_by(Bot.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_bot(session: AsyncSession, bot_id: int) -> Bot | None:
    return await session.get(Bot, bot_id)


async def is_name_exists(session: AsyncSession,
                         name: str,
                         exclude_bot_id: int | None = None) -> bool:
    query = select(Bot).where(Bot.name == name)
    if exclude_bot_id is not None:
        query = query.where(Bot.id != exclude_bot_id)
    return bool(await session.scalar(query))
    

async def create_bot(bot: BotCreate, session: AsyncSession) -> Bot:
    # Проверка перед созданием
    if await is_name_exists(session, bot.name):
        raise BotNameConflict()

    db_bot = Bot(**bot.model_dump())
    session.add(db_bot)
    await session.commit()
    await session.refresh(db_bot)
    return db_bot


async def update_bot(bot_update: BotUpdate | BotPatch,
                      bot: Bot,
                      session: AsyncSession,
                      partial: bool = False, ) -> Bot:

    update_data = bot_update.model_dump(exclude_unset=partial)

    if "name" in update_data and await is_name_exists(session, update_data["name"], bot.id):
        raise BotNameConflict()

    for name, value in update_data.items():
        setattr(bot, name, value)

    await session.commit()
    return bot


async def delete_bot(bot: Bot, session: AsyncSession) -> None:
    await session.delete(bot)
    await session.commit()


async def get_bots_by_filters(
    session: AsyncSession,
    filters: dict | None = None,
    time_filters: dict | None = None
) -> Sequence[Bot]:
    stmt = apply_filters(Bot, filters, time_filters)
    result = await session.scalars(stmt)
    return result.all()
    
