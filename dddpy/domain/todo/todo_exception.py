"""Todo exception"""


class TodoNotFoundError(Exception):
    """TodoNotFoundError is an error that occurs when a Todo is not found."""

    message = 'The Todo you specified does not exist.'

    def __str__(self):
        return TodoNotFoundError.message


class TodoNotStartedError(Exception):
    """TodoNotStartedError is an error that occurs when a Todo is not started."""

    message = 'The Todo is not started.'

    def __str__(self):
        return TodoNotStartedError.message


class TodoAlreadyCompletedError(Exception):
    """TodoIsbnAlreadyCompletedError is an error that occurs when a Todo is already completed."""

    message = 'The Todo is already completed.'

    def __str__(self):
        return TodoAlreadyCompletedError.message


class TodoAlreadyStartedError(Exception):
    """TodoIsbnAlreadyStartedError is an error that occurs when a Todo is already started."""

    message = 'The Todo is already started.'

    def __str__(self):
        return TodoAlreadyStartedError.message
