#
class Book:
    """Book represents your collection of books as an entity."""

    def __init__(self, isbn: str, title: str, page: int, read_page: int = 0):
        self.isbn: str = isbn
        self.title: str = title
        self.page: int = page
        self._read_page: int = read_page

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Book):
            return self.isbn == o.isbn

        return False

    @property
    def read_page(self):
        return self._read_page

    @read_page.setter
    def read_page(self, p: int):
        if p < 0 or p > self.page:
            raise ValueError(f"read_page must be between 0 and {self.page}.")

        self._read_page = p

    def is_already_read(self) -> bool:
        return self.page == self._read_page
