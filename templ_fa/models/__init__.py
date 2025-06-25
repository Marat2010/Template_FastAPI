# template_FA/models/__init__.py.template
__all__ = (
    "db_helper",
    "Base",
    "Book",
)
from .db_helper import db_helper
from .base import Base
from .book import Book

