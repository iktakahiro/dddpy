from typing import cast

from pydantic import BaseModel, Field

from dddpy.domain.book import Book


class BookReadModel(BaseModel):
    """BookReadModel represents data structure as a read model."""

    id: str = Field(examples=['vytxeTZskVKR7C7WgdSP3d'])
    isbn: str = Field(examples=['978-0321125217'])
    title: str = Field(
        examples=['Domain-Driven Design: Tackling Complexity in the Heart of Softwares']
    )
    page: int = Field(ge=0, examples=[320])
    read_page: int = Field(ge=0, examples=[120])
    created_at: int = Field(examples=[1136214245000])
    updated_at: int = Field(examples=[1136214245000])

    class Config:
        from_attributes = True

    @staticmethod
    def from_entity(book: Book) -> 'BookReadModel':
        return BookReadModel(
            id=book.book_id,
            isbn=book.isbn.value,
            title=book.title,
            page=book.page,
            read_page=book.read_page,
            created_at=cast(int, book.created_at),
            updated_at=cast(int, book.updated_at),
        )
