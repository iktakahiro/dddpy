from abc import ABC, abstractmethod
from typing import List, Optional

from dddpy.domain.book import Book


class BookRepository(ABC):
    """BookRepository defines a repository interface for Book entity."""

    @abstractmethod
    def create(self, book: Book) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def update(self, book: Book) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: str):
        raise NotImplementedError
