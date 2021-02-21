from abc import ABC, abstractmethod
from typing import List, Optional

from dddpy.domain.book.book import Book
from dddpy.domain.book.book_repository import BookRepository


class BookUseCaseUnitOfWork(ABC):
    """BookUseCaseUnitOfWork defines an interface of BookUseCase based on Unit of Work pattern."""

    book_repository: BookRepository

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass


class BookUseCase(ABC):
    """BookUseCase defines a usecase inteface related Book entity."""

    @abstractmethod
    def create_book(self, isbn: str, title: str, page: int) -> Book:
        pass

    @abstractmethod
    def fetch_book_by_id(self, id: str) -> Optional[Book]:
        pass

    @abstractmethod
    def fetch_books(self) -> List[Book]:
        pass


class BookUseCaseImpl(BookUseCase):
    """BookUseCaseImpl implements a usecase inteface related Book entity."""

    def __init__(self, uow: BookUseCaseUnitOfWork):
        self.uow: BookUseCaseUnitOfWork = uow

    def create_book(
        self,
        isbn: str,
        title: str,
        page: int,
    ) -> Book:
        book = Book(
            isbn=isbn,
            title=title,
            page=page,
        )
        try:
            self.uow.begin()

            self.uow.book_repository.create(book)
            created_book = self.fetch_book_by_id(isbn)

            if created_book is None:
                raise Exception

            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return created_book

    def fetch_book_by_isbn(self, isbn: str) -> Optional[Book]:
        try:
            book = self.uow.book_repository.find_by_isbn(isbn)
        except:
            raise

        return book

    def fetch_books(self) -> List[Book]:
        try:
            books = self.uow.book_repository.find_all()
        except:
            raise

        return books
