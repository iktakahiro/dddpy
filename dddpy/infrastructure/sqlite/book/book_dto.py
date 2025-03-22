from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from dddpy.domain.book import Book, Isbn
from dddpy.infrastructure.sqlite.database import Base
from dddpy.usecase.book import BookReadModel


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class BookDTO(Base):
    """BookDTO is a data transfer object associated with Book entity."""

    __tablename__ = 'book'
    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    isbn: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    page: Mapped[int] = mapped_column(nullable=False)
    read_page: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[int] = mapped_column(index=True, nullable=False)
    updated_at: Mapped[int] = mapped_column(index=True, nullable=False)

    def to_entity(self) -> Book:
        return Book(
            book_id=self.id,
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
    def from_entity(book: Book) -> 'BookDTO':
        now = unixtimestamp()
        return BookDTO(
            id=book.book_id,
            isbn=book.isbn.value,
            title=book.title,
            page=book.page,
            read_page=book.read_page,
            created_at=now,
            updated_at=now,
        )
