from abc import ABC, abstractmethod
from typing import List, Optional

from dddpy.domain.book.book import Book
from dddpy.usecase.transaction_manager import TransactionManager


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

    def __init__(self, tx_manager: TransactionManager):
        self.tx_manager: TransactionManager = tx_manager

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
            self.tx_manager.begin()

            self.tx_manager.book_repository.create(book)
            created_book = self.fetch_book_by_id(isbn)

            if created_book is None:
                raise Exception

            self.tx_manager.commit()
        except:
            self.tx_manager.rollback()
            raise


        return created_book

    def fetch_book_by_isbn(self, isbn: str) -> Optional[Book]:
        try:
            book = self.tx_manager.book_repository.find_by_isbn(isbn)
        except:
            raise

        return book

    def fetch_books(self) -> List[Book]:
        try:
            books = self.tx_manager.book_repository.find_all()
        except:
            raise

        return books
