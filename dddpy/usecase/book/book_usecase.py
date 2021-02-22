from abc import ABC, abstractmethod
from typing import List, Optional

import shortuuid

from dddpy.domain.book.book import Book
from dddpy.domain.book.book_exeption import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)
from dddpy.domain.book.book_repository import BookRepository


class BookUseCaseUnitOfWork(ABC):
    """BookUseCaseUnitOfWork defines an interface of BookUseCase based on Unit of Work pattern."""

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


class BookUseCase(ABC):
    """BookUseCase defines a usecase inteface related Book entity."""

    @abstractmethod
    def create_book(
        self,
        isbn: str,
        title: str,
        page: int,
    ) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def fetch_book_by_id(self, id: str) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def fetch_book_by_isbn(self, isbn: str) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def fetch_books(self) -> List[Book]:
        raise NotImplementedError

    @abstractmethod
    def delete_book_by_id(self, id: str):
        raise NotImplementedError


class BookUseCaseImpl(BookUseCase):
    """BookUseCaseImpl implements usecases related Book entity."""

    def __init__(self, uow: BookUseCaseUnitOfWork):
        self.uow: BookUseCaseUnitOfWork = uow

    def create_book(
        self,
        isbn: str,
        title: str,
        page: int,
    ) -> Optional[Book]:

        id = shortuuid.uuid()
        book = Book(
            id=id,
            isbn=isbn,
            title=title,
            page=page,
        )
        try:
            existing_book = self.uow.book_repository.find_by_isbn(isbn)
            if existing_book is not None:
                raise BookIsbnAlreadyExistsError

            self.uow.book_repository.create(book)
            self.uow.commit()

            created_book = self.uow.book_repository.find_by_id(id)

        except:
            self.uow.rollback()
            raise

        return created_book

    def fetch_book_by_id(self, id: str) -> Optional[Book]:
        try:
            book = self.uow.book_repository.find_by_id(id)
            if book is None:
                raise BookNotFoundError
        except:
            raise

        return book

    def fetch_book_by_isbn(self, isbn: str) -> Optional[Book]:
        try:
            book = self.uow.book_repository.find_by_isbn(isbn)
            if book is None:
                raise BookNotFoundError
        except:
            raise

        return book

    def fetch_books(self) -> List[Book]:
        try:
            books = self.uow.book_repository.find_all()
            if books is None or len(books) == 0:
                raise BooksNotFoundError
        except:
            raise

        return books

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
