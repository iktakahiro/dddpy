class BookNotFoundError(Exception):
    message = "The spcecified book does not exist."
    def __str__(self):
        return BookNotFoundError.message


class BooksNotFoundError(Exception):
    message = "No books were found."
    def __str__(self):
        return BooksNotFoundError.message


class BookAlreadyExistsError(Exception):
    message = "The spcecified book already exists."
    def __str__(self):
        return BookAlreadyExistsError.message
