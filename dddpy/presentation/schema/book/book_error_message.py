from pydantic import BaseModel, Field

from dddpy.domain.book import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)


class ErrorMessageBookNotFound(BaseModel):
    detail: str = Field(example=BookNotFoundError.message)


class ErrorMessageBooksNotFound(BaseModel):
    detail: str = Field(example=BooksNotFoundError.message)


class ErrorMessageBookIsbnAlreadyExists(BaseModel):
    detail: str = Field(example=BookIsbnAlreadyExistsError.message)
