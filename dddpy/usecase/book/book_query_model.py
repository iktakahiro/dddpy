from dataclasses import dataclass
from typing import cast

from dddpy.domain.book.book import Book


@dataclass(frozen=True)
class BookQueryModel:
    id: str
    isbn: str
    title: str
    page: int
    read_page: int
    created_at: int
    updated_at: int


def from_entiry_to_query_model(book: Book) -> BookQueryModel:
    return BookQueryModel(
        id=book.id,
        isbn=book.isbn.value,
        title=book.title,
        page=book.page,
        read_page=book.read_page,
        created_at=cast(int, book.created_at),
        updated_at=cast(int, book.updated_at),
    )
