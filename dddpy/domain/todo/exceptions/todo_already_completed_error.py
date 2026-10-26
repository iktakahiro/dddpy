"""Define exception for completing an already completed todo."""


class TodoAlreadyCompletedError(ValueError):
    """Raise when changing a todo that is already completed.

    Subclasses ``ValueError`` so that callers who caught the ``ValueError``
    previously raised by ``Todo.complete()`` keep working.
    """

    message = 'The Todo is already completed.'

    def __str__(self):
        """Return the default human-readable error message."""
        return TodoAlreadyCompletedError.message
