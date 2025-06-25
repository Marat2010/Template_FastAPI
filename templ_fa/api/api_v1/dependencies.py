# template_FA/api/api_v1/dependencies.py.template
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper, Book
from crud import book as book_crud


async def book_by_id(
    book_id: Annotated[int, Path],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Book:

    book = await book_crud.get_book(session=session, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book id: {book_id} not found!")

    return book

