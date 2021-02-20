from pydantic import BaseModel


class BookCreateSchema(BaseModel):
    """BookCreateSchema represents data structure of a post request to create a book."""

    isbn: str
    title: str
    page: int


class BookReadSchema(BaseModel):
    """BookReadSchema represents data structure of a get request to fetch books."""

    isbn: str
    title: str
    page: int
    read_page: int
    created_at: int
    updated_at: int
