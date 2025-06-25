from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.exceptions import BookNameConflict
from models import Book
from schemas.book import BookCreate, BookUpdate, BookPatch 

from utils.filters import apply_filters


async def get_all_book(session: AsyncSession) -> Sequence[Book]:
    stmt = select(Book).order_by(Book.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_book(session: AsyncSession, book_id: int) -> Book | None:
    return await session.get(Book, book_id)


async def is_name_exists(session: AsyncSession,
                         name: str,
                         exclude_book_id: int | None = None) -> bool:
    query = select(Book).where(Book.name == name)
    if exclude_book_id is not None:
        query = query.where(Book.id != exclude_book_id)
    return bool(await session.scalar(query))
    

async def create_book(book: BookCreate, session: AsyncSession) -> Book:
    # Проверка перед созданием
    if await is_name_exists(session, book.name):
        raise BookNameConflict()

    db_book = Book(**book.model_dump())
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book


async def update_book(book_update: BookUpdate | BookPatch,
                      book: Book,
                      session: AsyncSession,
                      partial: bool = False, ) -> Book:

    update_data = book_update.model_dump(exclude_unset=partial)

    if "name" in update_data and await is_name_exists(session, update_data["name"], book.id):
        raise BookNameConflict()

    for name, value in update_data.items():
        setattr(book, name, value)

    await session.commit()
    return book


async def delete_book(book: Book, session: AsyncSession) -> None:
    await session.delete(book)
    await session.commit()


async def get_books_by_filters(
    session: AsyncSession,
    filters: dict | None = None,
    time_filters: dict | None = None
) -> Sequence[Book]:
    stmt = apply_filters(Book, filters, time_filters)
    result = await session.scalars(stmt)
    return result.all()
    
