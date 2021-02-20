from abc import ABC, abstractmethod
from typing import List, Optional

from dddpy.domain.book.book import Book


class BookRepository(ABC):
    """BookRepository defines a repository interface for Book entity."""

    @abstractmethod
    def create(self, book: Book) -> Book:
        pass

    @abstractmethod
    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        pass

    @abstractmethod
    def find_all(self) -> List[Book]:
        pass
