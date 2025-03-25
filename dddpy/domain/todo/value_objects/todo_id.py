"""Value objects for Todo identifier."""

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class TodoId:
    """Value object representing the identifier of a Todo"""

    value: UUID

    @staticmethod
    def generate() -> 'TodoId':
        """Generate a new ID"""
        return TodoId(uuid4())

    def __str__(self) -> str:
        return str(self.value)
