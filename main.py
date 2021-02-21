from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm.session import Session

from dddpy.infrastructure.sqlite.book.book_repository import BookRepositoryWithSession
from dddpy.infrastructure.sqlite.database import SessionLocal
from dddpy.presentation.schema.book.book_schema import BookCreateSchema, BookReadSchema
from dddpy.usecase.book.book_usecase import (
    BookUseCase,
    BookUseCaseImpl,
    BookUseCaseUnitOfWork,
)

app = FastAPI()


def get_session() -> Session:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def book_usecase(session: Session = Depends(get_session)) -> BookUseCase:
    uow: BookUseCaseUnitOfWork = BookRepositoryWithSession(session)
    return BookUseCaseImpl(uow)


@app.post("/books", response_model=BookReadSchema)
async def create_book(
    data: BookCreateSchema,
    book_usecase: BookUseCase = Depends(book_usecase),
):
    book = book_usecase.create_book(
        isbn=data.isbn,
        title=data.title,
        page=data.page,
    )

    return book


@app.get("/books", response_model=List[BookReadSchema])
async def get_books(
    book_usecase: BookUseCase = Depends(book_usecase),
):
    books = book_usecase.create_book()
    if books is None or len(books) == 0:
        raise HTTPException(status_code=404, detail="books do not exist.")

    return books


@app.get("/books/{book_id}", response_model=BookReadSchema)
async def get_book(
    book_id: str,
    book_usecase: BookUseCase = Depends(book_usecase),
):
    book = book_usecase.fetch_book_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=404, detail="The spcecified book does not exist."
        )

    return book
