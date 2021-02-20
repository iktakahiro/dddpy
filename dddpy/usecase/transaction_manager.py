from abc import ABC, abstractmethod

from dddpy.domain.book.book_repository import BookRepository


class TransactionManager(ABC):
    """TransactionHandler deines an interface based on Unit of Work pattern."""

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
