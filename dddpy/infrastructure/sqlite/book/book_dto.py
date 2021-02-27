from datetime import datetime
from typing import Union

from sqlalchemy import Column, Integer, String

from dddpy.domain.book import Book, Isbn
from dddpy.infrastructure.sqlite.database import Base
from dddpy.usecase.book import BookReadModel


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class BookDTO(Base):
    """BookDTO is a data transfer object associated with Book entity."""

    __tablename__ = "book"
    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    isbn: Union[str, Column] = Column(String(17), unique=True, nullable=False)
    title: Union[str, Column] = Column(String, nullable=False)
    page: Union[int, Column] = Column(Integer, nullable=False)
    read_page: Union[int, Column] = Column(Integer, nullable=False, default=0)
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> Book:
        return Book(
            id=self.id,
            isbn=Isbn(self.isbn),
            title=self.title,
            page=self.page,
            read_page=self.read_page,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_read_model(self) -> BookReadModel:
        return BookReadModel(
            id=self.id,
            isbn=self.isbn,
            title=self.title,
            page=self.page,
            read_page=self.read_page,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(book: Book) -> "BookDTO":
        now = unixtimestamp()
        return BookDTO(
            id=book.id,
            isbn=book.isbn.value,
            title=book.title,
            page=book.page,
            read_page=book.read_page,
            created_at=now,
            updated_at=now,
        )
