"""Domain model for ToDo entities and related value objects."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class ToDoStatus(Enum):
    """Value object representing the status of a ToDo"""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass(frozen=True)
class ToDoId:
    """Value object representing the identifier of a ToDo"""

    value: UUID

    @staticmethod
    def generate() -> "ToDoId":
        """Generate a new ID"""
        return ToDoId(uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class ToDoTitle:
    """Value object representing the title of a ToDo"""

    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Title is required")
        if len(self.value) > 100:
            raise ValueError("Title must be 100 characters or less")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ToDoDescription:
    """Value object representing the description of a ToDo"""

    value: str

    def __post_init__(self):
        if len(self.value) > 1000:
            raise ValueError("Description must be 1000 characters or less")

    def __str__(self) -> str:
        return self.value


class ToDo:
    """ToDo entity representing a task or item to be completed"""

    def __init__(
        self,
        title: ToDoTitle,
        description: Optional[ToDoDescription] = None,
    ):
        """
        Initialize a new ToDo entity.
        """
        self._id = ToDoId.generate()
        self._title = title
        self._description = description if description else None
        self._status = ToDoStatus.NOT_STARTED
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._completed_at = None

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, ToDo):
            return self.id == obj.id

        return False

    @property
    def id(self) -> ToDoId:
        """Get the ToDo's unique identifier"""
        return self._id

    @property
    def title(self) -> ToDoTitle:
        """Get the ToDo's title"""
        return self._title

    @property
    def description(self) -> Optional[ToDoDescription]:
        """Get the ToDo's description"""
        return self._description

    @property
    def status(self) -> ToDoStatus:
        """Get the ToDo's current status"""
        return self._status

    @property
    def created_at(self) -> datetime:
        """Get the ToDo's creation timestamp"""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get the ToDo's last update timestamp"""
        return self._updated_at

    @property
    def completed_at(self) -> Optional[datetime]:
        """Get the ToDo's completion timestamp"""
        return self._completed_at

    def update_title(self, new_title: ToDoTitle) -> None:
        """Update the ToDo's title"""
        self._title = new_title
        self._updated_at = datetime.now()

    def update_description(self, new_description: Optional[ToDoDescription]) -> None:
        """Update the ToDo's description"""
        self._description = new_description if new_description else None
        self._updated_at = datetime.now()

    def start(self) -> None:
        """Change the ToDo's status to in progress"""
        if self._status != ToDoStatus.NOT_STARTED:
            raise ValueError("Only not started ToDos can be started")

        self._status = ToDoStatus.IN_PROGRESS
        self._updated_at = datetime.now()

    def complete(self) -> None:
        """Change the ToDo's status to completed"""
        if self._status == ToDoStatus.COMPLETED:
            raise ValueError("Already completed")

        self._status = ToDoStatus.COMPLETED
        self._completed_at = datetime.now()
        self._updated_at = self._completed_at

    @property
    def is_completed(self) -> bool:
        """Check if the ToDo is completed"""
        return self._status == ToDoStatus.COMPLETED

    def is_overdue(self, deadline: datetime) -> bool:
        """
        Check if the ToDo is overdue based on the given deadline
        """
        if self.is_completed:
            return self._completed_at is not None and self._completed_at > deadline
        return False
