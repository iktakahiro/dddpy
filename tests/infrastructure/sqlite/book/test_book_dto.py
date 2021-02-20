import pytest

from dddpy.domain.book.book import Book
from dddpy.infrastructure.sqlite.book.book_dto import BookDTO, from_entity


class TestBookDTO:
    def test_to_entity_should_create_entity_instance(self):
        book_dto = BookDTO(
            isbn="978-0141983479",
            title="Bullshit Jobs",
            page=320,
            read_page=120,
        )

        book = book_dto.to_entity()

        assert book.isbn == "978-0141983479"
        assert book.title == "Bullshit Jobs"
        assert book.page == 320
        assert book.read_page == 120

    def test_from_entity_should_create_dto_instance(self):
        book = Book(
            isbn="978-0141983479",
            title="Bullshit Jobs",
            page=320,
            read_page=120,
        )

        book_dto = from_entity(book)

        assert book_dto.isbn == "978-0141983479"
        assert book_dto.title == "Bullshit Jobs"
        assert book_dto.page == 320
        assert book_dto.read_page == 120
