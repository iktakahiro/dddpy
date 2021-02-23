from pydantic import BaseModel, Field

from dddpy.domain.book.book_exception import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)
from dddpy.domain.book.isbn import Isbn


class BookCreateSchema(BaseModel):
    """BookCreateSchema represents data structure of a post request to create a book."""

    isbn: str = Field(example="978-0141983479")
    title: str = Field(example="Bullshit Jobs")
    page: int = Field(ge=0, example=320)


class BookUpdateSchema(BaseModel):
    """BookUpdateSchema represents data structure of a put request to update a book."""

    title: str = Field(example="Bullshit Jobs")
    page: int = Field(ge=0, example=320)
    read_page: int = Field(ge=0, example=120)


class BookReadSchema(BaseModel):
    """BookReadSchema represents data structure of a get request to fetch books."""

    id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    isbn: str = Field(example="978-0141983479")
    title: str = Field(example="Bullshit Jobs")
    page: int = Field(ge=0, example=320)
    read_page: int = Field(ge=0, example=120)
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)

    class Config:
        orm_mode = True


class ErrorMessageBookNotFound(BaseModel):
    detail: str = Field(example=BookNotFoundError.message)


class ErrorMessageBooksNotFound(BaseModel):
    detail: str = Field(example=BooksNotFoundError.message)


class ErrorMessageBookIsbnAlreadyExists(BaseModel):
    detail: str = Field(example=BookIsbnAlreadyExistsError.message)
