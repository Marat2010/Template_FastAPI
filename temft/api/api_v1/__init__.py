from fastapi import APIRouter
from core.config import settings

from .item import router as item_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    item_router,
    prefix=settings.api.v1.item,
    # prefix=settings.api.v1.item2,
)

