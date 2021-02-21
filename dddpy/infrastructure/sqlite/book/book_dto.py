from datetime import datetime

from sqlalchemy import Column, Integer, String, engine

from dddpy.domain.book.book import Book
from dddpy.infrastructure.sqlite.database import Base, create_tables


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class BookDTO(Base):
    """BookDTO is a data tranfer object associated with Book entity."""

    __tablename__ = "book"

    isbn = Column(
        String,
        primary_key=True,
        autoincrement=False,
    )
    title = Column(String, nullable=False)
    page = Column(Integer, nullable=False)
    read_page = Column(
        Integer,
        nullable=False,
        default=0,
    )
    created_at = Column(
        Integer,
        index=True,
        nullable=False,
        default=unixtimestamp(),
    )
    updated_at = Column(
        Integer,
        index=True,
        nullable=False,
        default=unixtimestamp(),
        onupdate=unixtimestamp(),
    )

    def to_entity(self) -> Book:
        return Book(
            isbn=self.isbn,
            title=self.title,
            page=self.page,
            read_page=self.read_page,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


def from_entity(book: Book) -> BookDTO:
    return BookDTO(
        isbn=book.isbn,
        title=book.title,
        page=book.page,
        read_page=book.read_page,
    )
