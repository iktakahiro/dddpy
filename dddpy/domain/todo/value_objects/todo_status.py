"""Value objects for Todo status."""

from enum import Enum


class TodoStatus(Enum):
    """Value object representing the status of a Todo"""

    NOT_STARTED = 'not_started'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

    def __str__(self) -> str:
        """Return the value of the enum member."""
        return self.value
