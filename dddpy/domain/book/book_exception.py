class BookNotFoundError(Exception):
    message = "The book you spcecified does not exist."

    def __str__(self):
        return BookNotFoundError.message


class BooksNotFoundError(Exception):
    message = "No books were found."

    def __str__(self):
        return BooksNotFoundError.message


class BookIsbnAlreadyExistsError(Exception):
    message = "The book with the ISBN code you specified already exists."

    def __str__(self):
        return BookIsbnAlreadyExistsError.message
