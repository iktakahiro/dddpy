from typing import Optional


class Book:
    """Book represents your collection of books as an entity."""

    def __init__(
        self,
        id: str,
        isbn: str,
        title: str,
        page: int,
        read_page: int = 0,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.id: str = id
        self.isbn: str = isbn
        self.title: str = title
        self.page: int = page
        self.read_page: int = read_page
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Book):
            return self.id == o.id

        return False

    @property
    def read_page(self):
        return self._read_page

    @read_page.setter
    def read_page(self, p: int):
        try:
            self._validate_read_page(p)
        except:
            raise

        self._read_page = p

    def _validate_read_page(self, read_page):
        if read_page < 0 or read_page > self.page:
            raise ValueError(f"read_page must be between 0 and {self.page}.")

    def is_already_read(self) -> bool:
        return self.page == self._read_page
