import logging
from logging import config
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm.session import Session

from dddpy.domain.book.book import Book
from dddpy.domain.book.book_exeption import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)
from dddpy.infrastructure.sqlite.book.book_repository import BookRepositoryWithSession
from dddpy.infrastructure.sqlite.database import SessionLocal, create_tables
from dddpy.presentation.schema.book.book_schema import (
    BookCreateSchema,
    BookReadSchema,
    BookUpdateSchema,
    ErrorMessageBookIsbnAlreadyExists,
    ErrorMessageBookNotFound,
    ErrorMessageBooksNotFound,
)
from dddpy.usecase.book.book_usecase import (
    BookUseCase,
    BookUseCaseImpl,
    BookUseCaseUnitOfWork,
)

config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

create_tables()


def get_session() -> Session:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def book_usecase(session: Session = Depends(get_session)) -> BookUseCase:
    uow: BookUseCaseUnitOfWork = BookRepositoryWithSession(session)
    return BookUseCaseImpl(uow)


@app.post(
    "/books",
    response_model=BookReadSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageBookIsbnAlreadyExists,
        },
    },
)
async def create_book(
    data: BookCreateSchema,
    book_usecase: BookUseCase = Depends(book_usecase),
):
    try:
        book = book_usecase.create_book(
            isbn=data.isbn,
            title=data.title,
            page=data.page,
        )
    except BookIsbnAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return book


@app.get(
    "/books",
    response_model=List[BookReadSchema],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBooksNotFound,
        },
    },
)
async def get_books(
    book_usecase: BookUseCase = Depends(book_usecase),
):
    try:
        books = book_usecase.fetch_books()
    except BooksNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return books


@app.get(
    "/books/{book_id}",
    response_model=BookReadSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBookNotFound,
        },
    },
)
async def get_book(
    id: str,
    book_usecase: BookUseCase = Depends(book_usecase),
):
    try:
        book = book_usecase.fetch_book_by_id(id)
    except BookNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return book


@app.put(
    "/books/{book_id}",
    response_model=BookReadSchema,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBookNotFound,
        },
    },
)
async def update_book(
    id: str,
    data: BookUpdateSchema,
    book_usecase: BookUseCase = Depends(book_usecase),
):
    try:
        updated_book = book_usecase.update_book(
            id, data.title, data.page, data.read_page
        )
    except BookNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return updated_book


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBookNotFound,
        },
    },
)
async def delete_book(
    id: str,
    book_usecase: BookUseCase = Depends(book_usecase),
):
    try:
        book_usecase.delete_book_by_id(id)
    except BookNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
