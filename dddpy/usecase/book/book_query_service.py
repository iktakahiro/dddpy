from abc import ABC, abstractmethod
from typing import List, Optional

from .book_query_model import BookReadModel


class BookQueryService(ABC):
    """BookQueryService defines a query service inteface related Book entity."""

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[BookReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[BookReadModel]:
        raise NotImplementedError
