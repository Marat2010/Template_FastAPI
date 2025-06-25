# template_FA/api/api_v1/__init__.py.template
from fastapi import APIRouter
from core.config import settings

from .bot import router as bot_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    bot_router,
    prefix=settings.api.v1.bot,
    # prefix=settings.api.v1.bot2,
)

