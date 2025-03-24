"""TodoNotFoundError exception"""


class TodoNotFoundError(Exception):
    """TodoNotFoundError is an error that occurs when a Todo is not found."""

    message = 'The Todo you specified does not exist.'

    def __str__(self):
        return TodoNotFoundError.message
