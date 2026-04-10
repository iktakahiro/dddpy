"""Define the Todo description value object."""

from dataclasses import dataclass

MAX_DESCRIPTION_LENGTH = 1000
DESCRIPTION_TOO_LONG_ERROR_MESSAGE = 'Description must be 1000 characters or less'


@dataclass(frozen=True)
class TodoDescription:
    """Represent the optional description for a todo item."""

    value: str

    def __post_init__(self):
        """Validate the description length constraints.

        Raises:
            ValueError: If the description exceeds 1000 characters.
        """
        if len(self.value) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(DESCRIPTION_TOO_LONG_ERROR_MESSAGE)

    def __str__(self) -> str:
        """Return the wrapped description string."""
        return self.value
