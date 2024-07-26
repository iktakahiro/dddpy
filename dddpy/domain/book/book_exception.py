# -*- coding: utf-8 -*-
"""Book exception"""


class BookNotFoundError(Exception):
    """BookNotFoundError is an error that occurs when a book is not found."""

    message = "The book you spcecified does not exist."

    def __str__(self):
        return BookNotFoundError.message


class BooksNotFoundError(Exception):
    """BooksNotFoundError is an error that occurs when books are not found."""

    message = "No books were found."

    def __str__(self):
        return BooksNotFoundError.message


class BookIsbnAlreadyExistsError(Exception):
    """BookIsbnAlreadyExistsError is an error that occurs when a book with the same ISBN code already exists."""

    message = "The book with the ISBN code you specified already exists."

    def __str__(self):
        return BookIsbnAlreadyExistsError.message
