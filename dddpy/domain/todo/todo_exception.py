"""ToDo exception"""


class ToDoNotFoundError(Exception):
    """ToDoNotFoundError is an error that occurs when a ToDo is not found."""

    message = 'The ToDo you specified does not exist.'

    def __str__(self):
        return ToDoNotFoundError.message


class ToDoNotStartedError(Exception):
    """ToDoNotStartedError is an error that occurs when a ToDo is not started."""

    message = 'The ToDo is not started.'

    def __str__(self):
        return ToDoNotStartedError.message


class ToDoAlreadyCompletedError(Exception):
    """ToDoIsbnAlreadyCompletedError is an error that occurs when a ToDo is already completed."""

    message = 'The ToDo is already completed.'

    def __str__(self):
        return ToDoAlreadyCompletedError.message


class ToDoAlreadyStartedError(Exception):
    """ToDoIsbnAlreadyStartedError is an error that occurs when a ToDo is already started."""

    message = 'The ToDo is already started.'

    def __str__(self):
        return ToDoAlreadyStartedError.message
