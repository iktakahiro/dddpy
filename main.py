import logging
from logging import config
from typing import Iterator, List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm.session import Session

from dddpy.domain.book import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BookRepository,
    BooksNotFoundError,
)
from dddpy.infrastructure.sqlite.book import (
    BookCommandUseCaseUnitOfWorkImpl,
    BookQueryServiceImpl,
    BookRepositoryImpl,
)
from dddpy.infrastructure.sqlite.database import SessionLocal, create_tables
from dddpy.presentation.schema.book.book_error_message import (
    ErrorMessageBookIsbnAlreadyExists,
    ErrorMessageBookNotFound,
    ErrorMessageBooksNotFound,
)
from dddpy.usecase.book import (
    BookCommandUseCase,
    BookCommandUseCaseImpl,
    BookCommandUseCaseUnitOfWork,
    BookCreateModel,
    BookQueryService,
    BookQueryUseCase,
    BookQueryUseCaseImpl,
    BookReadModel,
    BookUpdateModel,
)

config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

create_tables()


def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def book_query_usecase(session: Session = Depends(get_session)) -> BookQueryUseCase:
    book_query_service: BookQueryService = BookQueryServiceImpl(session)
    return BookQueryUseCaseImpl(book_query_service)


def book_command_usecase(session: Session = Depends(get_session)) -> BookCommandUseCase:
    book_repository: BookRepository = BookRepositoryImpl(session)
    uow: BookCommandUseCaseUnitOfWork = BookCommandUseCaseUnitOfWorkImpl(
        session, book_repository=book_repository
    )
    return BookCommandUseCaseImpl(uow)


@app.post(
    "/books",
    response_model=BookReadModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageBookIsbnAlreadyExists,
        },
    },
)
async def create_book(
    data: BookCreateModel,
    book_command_usecase: BookCommandUseCase = Depends(book_command_usecase),
):
    try:
        book = book_command_usecase.create_book(data)
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
    response_model=List[BookReadModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBooksNotFound,
        },
    },
)
async def get_books(
    book_query_usecase: BookQueryUseCase = Depends(book_query_usecase),
):
    try:
        books = book_query_usecase.fetch_books()

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if len(books) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BooksNotFoundError.message,
        )

    return books


@app.get(
    "/books/{book_id}",
    response_model=BookReadModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBookNotFound,
        },
    },
)
async def get_book(
    book_id: str,
    book_query_usecase: BookQueryUseCase = Depends(book_query_usecase),
):
    try:
        book = book_query_usecase.fetch_book_by_id(book_id)
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
    response_model=BookReadModel,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBookNotFound,
        },
    },
)
async def update_book(
    book_id: str,
    data: BookUpdateModel,
    book_command_usecase: BookCommandUseCase = Depends(book_command_usecase),
):
    try:
        updated_book = book_command_usecase.update_book(book_id, data)
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
    book_id: str,
    book_command_usecase: BookCommandUseCase = Depends(book_command_usecase),
):
    try:
        book_command_usecase.delete_book_by_id(book_id)
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
