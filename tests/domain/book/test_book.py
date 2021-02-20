import pytest

from dddpy.domain.book.book import Book


class TestBook:
    def test_constructor_should_create_instance(self):
        book = Book(isbn="978-0141983479", title="Bullshit Jobs", page=320)

        assert book.isbn == "978-0141983479"
        assert book.title == "Bullshit Jobs"
        assert book.page == 320
        assert book.read_page == 0

    @pytest.mark.parametrize(
        "read_page",
        [
            (0),
            (1),
            (320),
        ],
    )
    def test_read_page_setter_should_update_value(self, read_page):
        book = Book(isbn="978-0141983479", title="Bullshit Jobs", page=320)

        book.read_page = read_page

        assert book.read_page == read_page

    @pytest.mark.parametrize(
        "read_page",
        [
            (321),
            (-1),
        ],
    )
    def test_read_page_setter_should_throw_value_error_when_params_are_invalid(
        self, read_page
    ):
        book = Book(isbn="978-0141983479", title="Bullshit Jobs", page=320)

        with pytest.raises(ValueError):
            book.read_page = read_page

    @pytest.mark.parametrize(
        "read_page, expected",
        [
            (0, False),
            (319, False),
            (320, True),
        ],
    )
    def test_is_already_read_should_true_when_read_page_has_reached_last_page(
        self, read_page, expected
    ):

        book = Book(isbn="978-0141983479", title="Bullshit Jobs", page=320)
        book.read_page = read_page

        assert book.is_already_read() == expected
