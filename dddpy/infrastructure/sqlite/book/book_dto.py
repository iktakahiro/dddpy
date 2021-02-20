from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from dddpy.domain.book.book import Book

Base = declarative_base()


class BookDTO(Base):
    """BookDTO is a data tranfer object associated with Book entity."""

    __tablename__ = "book"

    isbn = Column(
        String,
        primary_key=True,
    )
    title = Column(
        String,
        nullable=False,
    )
    page = Column(
        Integer,
        nullable=False,
    )
    read_page = Column(
        Integer,
        nullable=False,
        default=0,
    )
    created_at = Column(
        Integer,
        index=True,
        nullable=False,
        default=datetime.utcnow(),
    )
    updated_at = Column(
        Integer,
        index=True,
        nullable=False,
        onupdate=datetime.utcnow(),
    )

    def __init__(
        self,
        isbn: str,
        title: str,
        page: int,
        read_page: int,
    ):
        self.isbn: str = isbn
        self.title: str = title
        self.page: int = page
        self.read_page: int = read_page

    def to_entity(self) -> Book:
        return Book(
            isbn=self.isbn,
            title=self.title,
            page=self.page,
            read_page=self.read_page,
        )


def from_entity(book: Book) -> BookDTO:
    return BookDTO(
        isbn=book.isbn,
        title=book.title,
        page=book.page,
        read_page=book.read_page,
    )
