"""TodoAlreadyCompletedError exception"""


class TodoAlreadyCompletedError(Exception):
    """TodoAlreadyCompletedError is an error that occurs when a Todo is already completed."""

    message = 'The Todo is already completed.'

    def __str__(self):
        return TodoAlreadyCompletedError.message
