from unittest.mock import MagicMock, Mock

import pytest

from dddpy.domain.book import BookNotFoundError
from dddpy.infrastructure.sqlite.book import BookQueryServiceImpl
from dddpy.usecase.book import BookQueryUseCaseImpl, BookReadModel


class TestBookQueryUseCase:
    def test_fetch_book_by_id_should_return_book(self):

        session = MagicMock()
        book_query_service = BookQueryServiceImpl(session)
        book_query_service.find_by_id = Mock(
            return_value=BookReadModel(
                id="cPqw4yPVUM3fA9sqzpZmkL",
                isbn="978-0321125217",
                title="Domain-Driven Design: Tackling Complexity in the Heart of Software",
                page=560,
                read_page=126,
                created_at=1614051983128,
                updated_at=1614056689464,
            )
        )

        book_query_usecase = BookQueryUseCaseImpl(book_query_service)

        book = book_query_usecase.fetch_book_by_id("cPqw4yPVUM3fA9sqzpZmkL")

        assert (
            book.title
            == "Domain-Driven Design: Tackling Complexity in the Heart of Software"
        )

    def test_fetch_book_by_id_should_throw_book_not_found_error(self):

        session = MagicMock()
        book_query_service = BookQueryServiceImpl(session)
        book_query_service.find_by_id = Mock(side_effect=BookNotFoundError)

        book_query_usecase = BookQueryUseCaseImpl(book_query_service)

        with pytest.raises(BookNotFoundError):
            book_query_usecase.fetch_book_by_id("cPqw4yPVUM3fA9sqzpZmkL")

    def test_fetch_books_should_return_books(self):
        session = MagicMock()
        book_query_service = BookQueryServiceImpl(session)
        book_query_service.find_all = Mock(
            return_value=[
                BookReadModel(
                    id="cPqw4yPVUM3fA9sqzpZmkL",
                    isbn="978-0321125217",
                    title="Domain-Driven Design: Tackling Complexity in the Heart of Software",
                    page=560,
                    read_page=126,
                    created_at=1614051983128,
                    updated_at=1614056689464,
                )
            ]
        )

        book_query_usecase = BookQueryUseCaseImpl(book_query_service)
        books = book_query_usecase.fetch_books()

        assert len(books) == 1
        assert books[0].page == 560
