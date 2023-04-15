# -*- coding: utf-8 -*-
"""Book domain"""

from typing import Optional

from .isbn import Isbn


class Book:
    """Book represents your collection of books as an entity."""

    def __init__(
        self,
        book_id: str,
        isbn: Isbn,
        title: str,
        page: int,
        read_page: int = 0,
        created_at: Optional[int] = None,
        updated_at: Optional[int] = None,
    ):
        self.book_id: str = book_id
        self.isbn: Isbn = isbn
        self.title: str = title
        self.page: int = page
        self.read_page: int = read_page
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Book):
            return self.book_id == obj.book_id

        return False

    def is_already_read(self) -> bool:
        """Return True if the message has already been read, False otherwise."""
        return self.page == self.read_page
