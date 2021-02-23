from abc import ABC, abstractmethod
from typing import List, Optional

from dddpy.usecase.book.book_query_model import BookQueryModel


class BookQueryService(ABC):
    """BookQueryService defines a query service inteface related Book entity."""

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[BookQueryModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[BookQueryModel]:
        raise NotImplementedError
