"""This module provides the Todo entity representing a task or item to be completed."""

from datetime import datetime
from typing import Optional

from dddpy.domain.todo.value_objects import (
    TodoDescription,
    TodoId,
    TodoStatus,
    TodoTitle,
)


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

    def is_overdue(
        self, deadline: datetime, current_time: Optional[datetime] = None
    ) -> bool:
        """
        Check if the Todo is overdue based on the given deadline.
        A Todo is considered overdue if:
        1. It is not completed and the current time is past the deadline
        Note: Completed todos are never considered overdue

        Args:
            deadline: The deadline to check against
            current_time: The current time to use for comparison (defaults to now)
        """
        if self.is_completed:
            return False
        return (current_time or datetime.now()) > deadline

    @staticmethod
    def create(
        title: TodoTitle, description: Optional[TodoDescription] = None
    ) -> 'Todo':
        """Create a new Todo"""
        return Todo(TodoId.generate(), title, description)
