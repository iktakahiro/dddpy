"""Define the Todo title value object."""

from dataclasses import dataclass

MAX_TITLE_LENGTH = 100
TITLE_REQUIRED_ERROR_MESSAGE = 'Title is required'
TITLE_TOO_LONG_ERROR_MESSAGE = 'Title must be 100 characters or less'


@dataclass(frozen=True)
class TodoTitle:
    """Represent the title for a todo item."""

    value: str

    def __post_init__(self):
        """Validate the provided title string.

        Raises:
            ValueError: If the title is empty or longer than 100 characters.
        """
        if not self.value:
            raise ValueError(TITLE_REQUIRED_ERROR_MESSAGE)
        if len(self.value) > MAX_TITLE_LENGTH:
            raise ValueError(TITLE_TOO_LONG_ERROR_MESSAGE)

    def __str__(self) -> str:
        """Return the wrapped title string."""
        return self.value
