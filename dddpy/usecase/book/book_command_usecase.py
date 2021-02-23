from abc import ABC, abstractmethod
from typing import Optional, cast

import shortuuid

from dddpy.domain.book.book import Book
from dddpy.domain.book.book_exception import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
)
from dddpy.domain.book.book_repository import BookRepository
from dddpy.domain.book.isbn import Isbn
from dddpy.usecase.book.book_query_model import (
    BookQueryModel,
    from_entiry_to_query_model,
)


class BookCommandUseCaseUnitOfWork(ABC):
    """BookCommandUseCaseUnitOfWork defines an interface based on Unit of Work pattern."""

    book_repository: BookRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class BookCommandUseCase(ABC):
    """BookCommandUseCase defines a command usecase inteface related Book entity."""

    @abstractmethod
    def create_book(
        self, isbn_str: str, title: str, page: int
    ) -> Optional[BookQueryModel]:
        raise NotImplementedError

    @abstractmethod
    def update_book(
        self, id: str, title: str, page: int, read_page: int
    ) -> Optional[BookQueryModel]:
        raise NotImplementedError

    @abstractmethod
    def delete_book_by_id(self, id: str):
        raise NotImplementedError


class BookCommandUseCaseImpl(BookCommandUseCase):
    """BookCommandUseCaseImpl implements a command usecases related Book entity."""

    def __init__(
        self,
        uow: BookCommandUseCaseUnitOfWork,
    ):
        self.uow: BookCommandUseCaseUnitOfWork = uow

    def create_book(
        self, isbn_str: str, title: str, page: int
    ) -> Optional[BookQueryModel]:
        try:
            uuid = shortuuid.uuid()
            isbn = Isbn(isbn_str)
            book = Book(id=uuid, isbn=Isbn(isbn_str), title=title, page=page)

            existing_book = self.uow.book_repository.find_by_isbn(isbn.value)
            if existing_book is not None:
                raise BookIsbnAlreadyExistsError

            self.uow.book_repository.create(book)
            self.uow.commit()

            created_book = self.uow.book_repository.find_by_id(uuid)
        except:
            self.uow.rollback()
            raise

        return from_entiry_to_query_model(cast(Book, created_book))

    def update_book(
        self, id: str, title: str, page: int, read_page: int
    ) -> Optional[BookQueryModel]:
        try:
            existing_book = self.uow.book_repository.find_by_id(id)
            if existing_book is None:
                raise BookNotFoundError

            book = Book(
                id=id,
                isbn=existing_book.isbn,
                title=title,
                page=page,
                read_page=read_page,
            )

            self.uow.book_repository.update(book)

            updated_book = self.uow.book_repository.find_by_id(book.id)

            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return from_entiry_to_query_model(cast(Book, updated_book))

    def delete_book_by_id(self, id: str):
        try:
            existing_book = self.uow.book_repository.find_by_id(id)
            if existing_book is None:
                raise BookNotFoundError

            self.uow.book_repository.delete_by_id(id)

            self.uow.commit()
        except:
            self.uow.rollback()
            raise
