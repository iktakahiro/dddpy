"""TodoNotStartedError exception"""


class TodoNotStartedError(Exception):
    """TodoNotStartedError is an error that occurs when a Todo is not started."""

    message = 'The Todo is not started.'

    def __str__(self):
        return TodoNotStartedError.message
