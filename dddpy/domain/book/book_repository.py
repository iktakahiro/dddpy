from abc import ABC, abstractmethod
from typing import List

from dddpy.domain.book.book import Book


class BookRepository(ABC):
    """BookRepository defines a repository interface for Book entity."""

    @abstractmethod
    def create(self, book: Book):
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Book:
        pass

    @abstractmethod
    def find_all(self) -> List[Book]:
        pass
