"""Value objects for Todo title."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TodoTitle:
    """Value object representing the title of a Todo"""

    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError('Title is required')
        if len(self.value) > 100:
            raise ValueError('Title must be 100 characters or less')

    def __str__(self) -> str:
        return self.value
