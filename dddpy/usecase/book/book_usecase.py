from abc import ABC, abstractmethod
from typing import List

from dddpy.domain.book.book import Book
from dddpy.domain.book.book_repository import BookRepository


class BookUseCase(ABC):
    """BookUseCase defines a usecase inteface related Book entity."""

    @abstractmethod
    def create_book(self, book: Book):
        pass

    @abstractmethod
    def fetch_book_by_id(self, id: str) -> Book:
        pass

    @abstractmethod
    def fetch_books(self) -> List[Book]:
        pass


class BookUseCaseImpl(BookUseCase):
    """BookUseCaseImpl implements a usecase inteface related Book entity."""

    def __init__(self, book_repository: BookRepository):
        self.book_repository: BookRepository = book_repository

    def create_book(self, isbn: str, title: str):
        book = Book(
            isbn=isbn,
            title=title,
        )
        self.book_repository.create(book=book)

    def fetch_book_by_id(self, id: str) -> Book:
        return self.book_repository.find_by_id(id)

    def fetch_books(self) -> Book:
        return self.book_repository.find_all(id)
