"""TodoAlreadyStartedError exception"""


class TodoAlreadyStartedError(Exception):
    """TodoAlreadyStartedError is an error that occurs when a Todo is already started."""

    message = 'The Todo is already started.'

    def __str__(self):
        return TodoAlreadyStartedError.message
