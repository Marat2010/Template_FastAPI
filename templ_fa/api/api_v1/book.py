# template_FA/api/api_v1/book.py.template
from datetime import datetime

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from crud import book as book_crud
from .dependencies import book_by_id
from models import db_helper
from schemas.book import BookRead, BookCreate, BookUpdate, BookPatch

router = APIRouter()


@router.get("", response_model=list[BookRead])
async def get_books(session: AsyncSession = Depends(db_helper.session_getter)):
    book = await book_crud.get_all_book(session=session)
    return book


@router.get("/{book_id}/", response_model=BookRead)
async def get_book(book: BookRead = Depends(book_by_id)):
    return book
    
    
@router.post("", response_model=BookRead)
async def create_book(book_create: BookCreate,
                      session: AsyncSession = Depends(db_helper.session_getter)):
    return await book_crud.create_book(book=book_create, session=session)


@router.put("/{book_id}/")
async def update_book(book_update: BookUpdate,
                      book: BookRead = Depends(book_by_id),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    return await book_crud.update_book(
        book_update=book_update,
        book=book,
        session=session)


@router.patch("/{book_id}/")
async def update_book_partial(book_update: BookPatch,
                              book: BookRead = Depends(book_by_id),
                              session: AsyncSession = Depends(db_helper.session_getter)):
    return await book_crud.update_book(
        book_update=book_update,        
        book=book,
        session=session,
        partial=True)


@router.delete("/{book_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book: BookRead = Depends(book_by_id),
                      session: AsyncSession = Depends(db_helper.session_getter)) -> None:
    await book_crud.delete_book(book=book, session=session)


@router.get("/filter", response_model=list[BookRead])
async def filter_books(
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

    book = await book_crud.get_books_by_filters(
        session=session,
        filters=filters,
        time_filters=time_filters
    )
    return book


# ==========================================================
    # session: Annotated[AsyncSession, Depends(db_helper.session_getter)]

