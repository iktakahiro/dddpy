from pydantic import BaseModel, Field

from dddpy.domain.book import (
    BookIsbnAlreadyExistsError,
    BookNotFoundError,
    BooksNotFoundError,
)


class ErrorMessageBookNotFound(BaseModel):
    detail: str = Field(examples=[BookNotFoundError.message])


class ErrorMessageBooksNotFound(BaseModel):
    detail: str = Field(examples=[BooksNotFoundError.message])


class ErrorMessageBookIsbnAlreadyExists(BaseModel):
    detail: str = Field(examples=[BookIsbnAlreadyExistsError.message])
