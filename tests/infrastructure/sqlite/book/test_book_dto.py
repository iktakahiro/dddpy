import pytest

from dddpy.domain.book import Book, Isbn
from dddpy.infrastructure.sqlite.book import BookDTO


class TestBookDTO:
    def test_to_read_model_should_create_entity_instance(self):
        book_dto = BookDTO(
            id="book_01",
            isbn="978-0321125217",
            title="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
            page=560,
            read_page=120,
            created_at=1614007224642,
            updated_at=1614007224642,
        )

        book = book_dto.to_read_model()

        assert book.id == "book_01"
        assert book.isbn == "978-0321125217"
        assert (
            book.title
            == "Domain-Driven Design: Tackling Complexity in the Heart of Softwares"
        )
        assert book.page == 560
        assert book.read_page == 120

    def test_to_entity_should_create_entity_instance(self):
        book_dto = BookDTO(
            id="book_01",
            isbn="978-0321125217",
            title="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
            page=560,
            read_page=120,
            created_at=1614007224642,
            updated_at=1614007224642,
        )

        book = book_dto.to_entity()

        assert book.id == "book_01"
        assert book.isbn == Isbn("978-0321125217")
        assert (
            book.title
            == "Domain-Driven Design: Tackling Complexity in the Heart of Softwares"
        )
        assert book.page == 560
        assert book.read_page == 120

    def test_from_entity_should_create_dto_instance(self):
        book = Book(
            id="book_01",
            isbn=Isbn("978-0321125217"),
            title="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
            page=560,
            read_page=120,
            created_at=1614007224642,
            updated_at=1614007224642,
        )

        book_dto = BookDTO.from_entity(book)

        assert book_dto.id == "book_01"
        assert book_dto.isbn == "978-0321125217"
        assert (
            book_dto.title
            == "Domain-Driven Design: Tackling Complexity in the Heart of Softwares"
        )
        assert book_dto.page == 560
        assert book_dto.read_page == 120
