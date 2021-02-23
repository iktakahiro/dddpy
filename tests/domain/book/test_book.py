import pytest

from dddpy.domain.book import Book, Isbn


class TestBook:
    def test_constructor_should_create_instance(self):
        book = Book(
            id="book_01",
            isbn=Isbn("978-0321125217"),
            title="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
            page=560,
        )

        assert book.id == "book_01"
        assert book.isbn == Isbn("978-0321125217")
        assert (
            book.title
            == "Domain-Driven Design: Tackling Complexity in the Heart of Softwares"
        )
        assert book.page == 560
        assert book.read_page == 0

    def test_book_entity_should_be_identified_by_id(self):
        book_1 = Book(
            id="book_01",
            isbn=Isbn("978-0321125217"),
            title="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
            page=560,
            read_page=50,
        )

        book_2 = Book(
            id="book_01",
            isbn=Isbn("978-0321125217"),
            title="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
            page=560,
            read_page=120,
        )

        book_3 = Book(
            id="book_02",
            isbn=Isbn("978-0321125217"),
            title="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
            page=560,
            read_page=50,
        )

        assert book_1 == book_2
        assert book_1 != book_3

    @pytest.mark.parametrize(
        "read_page",
        [
            (0),
            (1),
            (320),
        ],
    )
    def test_read_page_setter_should_update_value(self, read_page):
        book = Book(
            id="book_01",
            isbn=Isbn("978-0321125217"),
            title="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
            page=560,
        )

        book.read_page = read_page

        assert book.read_page == read_page

    @pytest.mark.parametrize(
        "read_page, expected",
        [
            (0, False),
            (559, False),
            (560, True),
        ],
    )
    def test_is_already_read_should_true_when_read_page_has_reached_last_page(
        self, read_page, expected
    ):
        book = Book(
            id="book_01",
            isbn=Isbn("978-0321125217"),
            title="Domain-Driven Design: Tackling Complexity in the Heart of Softwares",
            page=560,
        )
        book.read_page = read_page

        assert book.is_already_read() == expected
