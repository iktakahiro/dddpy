from abc import ABC, abstractmethod
from typing import List, Optional

from dddpy.domain.book import BookNotFoundError, BooksNotFoundError

from .book_query_model import BookReadModel
from .book_query_service import BookQueryService


class BookQueryUseCase(ABC):
    """BookQueryUseCase defines a query usecase inteface related Book entity."""

    @abstractmethod
    def fetch_book_by_id(self, id: str) -> Optional[BookReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_books(self) -> List[BookReadModel]:
        raise NotImplementedError


class BookQueryUseCaseImpl(BookQueryUseCase):
    """BookQueryUseCaseImpl implements a query usecases related Book entity."""

    def __init__(self, book_query_service: BookQueryService):
        self.book_query_service: BookQueryService = book_query_service

    def fetch_book_by_id(self, id: str) -> Optional[BookReadModel]:
        try:
            book = self.book_query_service.find_by_id(id)
            if book is None:
                raise BookNotFoundError
        except:
            raise

        return book

    def fetch_books(self) -> List[BookReadModel]:
        try:
            books = self.book_query_service.find_all()
        except:
            raise

        return books
