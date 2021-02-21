from pydantic import BaseModel, Field

from dddpy.domain.book.book_exeption import (
    BookAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)


class BookBaseSchema(BaseModel):
    """BookBaseSchema represents base data structure of a book."""

    title: str = Field(example="Bullshit Jobs")
    page: int = Field(ge=0, example=320)


class BookCreateSchema(BookBaseSchema):
    """BookCreateSchema represents data structure of a post request to create a book."""

    isbn: str = Field(example="978-0141983479")

    pass


class BookUpdateSchema(BookBaseSchema):
    """BookUpdateSchema represents data structure of a put request to update a book."""

    pass


class BookReadSchema(BookBaseSchema):
    """BookReadSchema represents data structure of a get request to fetch books."""

    read_page: int = Field(ge=0, example=120)
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)


class BookNotFoundErrorMessage(BaseModel):
    detail: str = Field(example=BookNotFoundError.message)


class BooksNotFoundErrorMessage(BaseModel):
    detail: str = Field(example=BooksNotFoundError.message)


class BookAlreadyExistsErrorMessage(BaseModel):
    detail: str = Field(example=BookAlreadyExistsError.message)
