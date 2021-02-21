class BookNotFoundError(Exception):
    message = "The spcecified book does not exist."


class BooksNotFoundError(Exception):
    message = "No books were found."


class BookAlreadyExistsError(Exception):
    message = "The spcecified book already exists."
