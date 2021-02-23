import pytest

from dddpy.domain.book.book import Book
from dddpy.domain.book.isbn import Isbn
from dddpy.infrastructure.sqlite.book.book_dto import BookDTO, from_entity


class TestBookDTO:
    def test_to_query_model_should_create_entity_instance(self):
        book_dto = BookDTO(
            id="book_01",
            isbn="978-0141983479",
            title="Bullshit Jobs",
            page=320,
            read_page=120,
        )

        book = book_dto.to_query_model()

        assert book.id == "book_01"
        assert book.isbn == "978-0141983479"
        assert book.title == "Bullshit Jobs"
        assert book.page == 320
        assert book.read_page == 120

    def test_to_entiry_should_create_entity_instance(self):
        book_dto = BookDTO(
            id="book_01",
            isbn="978-0141983479",
            title="Bullshit Jobs",
            page=320,
            read_page=120,
        )

        book = book_dto.to_entiry()

        assert book.id == "book_01"
        assert book.isbn == Isbn("978-0141983479")
        assert book.title == "Bullshit Jobs"
        assert book.page == 320
        assert book.read_page == 120

    def test_from_entity_should_create_dto_instance(self):
        book = Book(
            id="book_01",
            isbn=Isbn("978-0141983479"),
            title="Bullshit Jobs",
            page=320,
            read_page=120,
        )

        book_dto = from_entity(book)

        assert book_dto.id == "book_01"
        assert book_dto.isbn == "978-0141983479"
        assert book_dto.title == "Bullshit Jobs"
        assert book_dto.page == 320
        assert book_dto.read_page == 120
