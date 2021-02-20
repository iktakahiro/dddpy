from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm.session import Session

from dddpy.domain.book.book import Book
from dddpy.domain.book.book_repository import BookRepository
from dddpy.infrastructure.sqlite.book.book_repository import BookRepositoryImpl
from dddpy.infrastructure.sqlite.database import SessionLocal
from dddpy.infrastructure.sqlite.transaction_manager import SqlAlchemyTransactionManager
from dddpy.presentation.book.book_schema import BookCreateSchema, BookReadSchema
from dddpy.usecase.book.book_usecase import BookUseCaseImpl
from dddpy.usecase.transaction_manager import TransactionManager

app = FastAPI()

book_repository: BookRepository = BookRepositoryImpl()


def get_tx_manager() -> TransactionManager:
    db = SessionLocal()
    return SqlAlchemyTransactionManager(db)


@app.post("/books", response_model=BookReadSchema)
async def create_book(
    data: BookCreateSchema,
    tx_manager: TransactionManager = Depends(get_tx_manager),
):
    book_usecase = BookUseCaseImpl(tx_manager)

    book = book_usecase.create_book(
        isbn=data.isbn,
        title=data.title,
        page=data.page,
    )

    return book


@app.get("/books", response_model=List[BookReadSchema])
async def get_books(
    tx_manager: TransactionManager = Depends(get_tx_manager),
):
    book_usecase = BookUseCaseImpl(tx_manager)

    books = book_usecase.create_book()
    if books is None or len(books) == 0:
        raise HTTPException(status_code=404, detail="books do not exist.")

    return books


@app.get("/books/{book_id}", response_model=BookReadSchema)
async def get_book(
    book_id: str,
    tx_manager: TransactionManager = Depends(get_tx_manager),
):
    book_usecase = BookUseCaseImpl(tx_manager)

    book = book_usecase.fetch_book_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=404, detail="The spcecified book does not exist."
        )

    return book
