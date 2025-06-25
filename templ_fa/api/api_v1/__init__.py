# template_FA/api/api_v1/__init__.py.template
from fastapi import APIRouter
from core.config import settings

from .book import router as book_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    book_router,
    prefix=settings.api.v1.book,
    # prefix=settings.api.v1.book2,
)

