"""Domain model for Todo entities and related value objects."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class TodoStatus(Enum):
    """Value object representing the status of a Todo"""

    NOT_STARTED = 'not_started'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


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


@dataclass(frozen=True)
class TodoDescription:
    """Value object representing the description of a Todo"""

    value: str

    def __post_init__(self):
        if len(self.value) > 1000:
            raise ValueError('Description must be 1000 characters or less')

    def __str__(self) -> str:
        return self.value


class Todo:
    """Todo entity representing a task or item to be completed"""

    def __init__(
        self,
        id: TodoId,
        title: TodoTitle,
        description: Optional[TodoDescription] = None,
        status: TodoStatus = TodoStatus.NOT_STARTED,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
        completed_at: Optional[datetime] = None,
    ):
        """
        Initialize a new Todo entity.
        """
        self._id = id
        self._title = title
        self._description = description
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at
        self._completed_at = completed_at

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Todo):
            return self.id == obj.id

        return False

    @property
    def id(self) -> TodoId:
        """Get the Todo's unique identifier"""
        return self._id

    @property
    def title(self) -> TodoTitle:
        """Get the Todo's title"""
        return self._title

    @property
    def description(self) -> Optional[TodoDescription]:
        """Get the Todo's description"""
        return self._description

    @property
    def status(self) -> TodoStatus:
        """Get the Todo's current status"""
        return self._status

    @property
    def created_at(self) -> datetime:
        """Get the Todo's creation timestamp"""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get the Todo's last update timestamp"""
        return self._updated_at

    @property
    def completed_at(self) -> Optional[datetime]:
        """Get the Todo's completion timestamp"""
        return self._completed_at

    def update_title(self, new_title: TodoTitle) -> None:
        """Update the Todo's title"""
        self._title = new_title
        self._updated_at = datetime.now()

    def update_description(self, new_description: Optional[TodoDescription]) -> None:
        """Update the Todo's description"""
        self._description = new_description if new_description else None
        self._updated_at = datetime.now()

    def start(self) -> None:
        """Change the Todo's status to in progress"""
        if self._status != TodoStatus.NOT_STARTED:
            raise ValueError('Only not started Todos can be started')

        self._status = TodoStatus.IN_PROGRESS
        self._updated_at = datetime.now()

    def complete(self) -> None:
        """Change the Todo's status to completed"""
        if self._status == TodoStatus.COMPLETED:
            raise ValueError('Already completed')

        self._status = TodoStatus.COMPLETED
        self._completed_at = datetime.now()
        self._updated_at = self._completed_at

    @property
    def is_completed(self) -> bool:
        """Check if the Todo is completed"""
        return self._status == TodoStatus.COMPLETED

    def is_overdue(self, deadline: datetime) -> bool:
        """
        Check if the Todo is overdue based on the given deadline
        """
        if self.is_completed:
            return self._completed_at is not None and self._completed_at > deadline
        return False

    @staticmethod
    def create(
        title: TodoTitle, description: Optional[TodoDescription] = None
    ) -> 'Todo':
        """Create a new Todo"""
        return Todo(TodoId.generate(), title, description)
