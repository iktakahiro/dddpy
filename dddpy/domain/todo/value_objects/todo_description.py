"""Value objects for Todo description."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TodoDescription:
    """Value object representing the description of a Todo"""

    value: str

    def __post_init__(self):
        if len(self.value) > 1000:
            raise ValueError('Description must be 1000 characters or less')

    def __str__(self) -> str:
        return self.value
