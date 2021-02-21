from pydantic import BaseModel


class BookBaseSchema(BaseModel):
    """BookBaseSchema represents base data structure of a book."""

    isbn: str
    title: str
    page: int


class BookCreateSchema(BookBaseSchema):
    """BookCreateSchema represents data structure of a post request to create a book."""

    pass


class BookReadSchema(BookBaseSchema):
    """BookReadSchema represents data structure of a get request to fetch books."""

    read_page: int
    created_at: int
    updated_at: int
