"""Define the Todo entity used throughout the domain layer."""

from datetime import datetime
from typing import Optional

from dddpy.domain.todo.value_objects import (
    TodoDescription,
    TodoId,
    TodoStatus,
    TodoTitle,
)


class Todo:
    """Represent a todo item tracked by the domain.

    Attributes:
        _id: Unique identifier for the todo.
        _title: Title describing the todo.
        _description: Optional detailed description.
        _status: Current lifecycle status.
        _created_at: Timestamp when the todo was created.
        _updated_at: Timestamp when the todo was last updated.
        _completed_at: Optional timestamp when the todo was completed.
    """

    def __init__(
        self,
        id: TodoId,
        title: TodoTitle,
        description: Optional[TodoDescription] = None,
        status: TodoStatus = TodoStatus.NOT_STARTED,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
    ):
        """Initialize a todo domain entity.

        Args:
            id: Identifier for the todo.
            title: Title describing the todo.
            description: Optional longer description.
            status: Initial lifecycle status.
            created_at: Creation timestamp in UTC.
            updated_at: Last updated timestamp in UTC.
            completed_at: Optional completion timestamp in UTC.
        """
        self._id = id
        self._title = title
        self._description = description
        self._status = status
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or datetime.now()
        self._completed_at = completed_at

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Todo):
            return self.id == obj.id

        return False

    @property
    def id(self) -> TodoId:
        """Return the todo's unique identifier."""
        return self._id

    @property
    def title(self) -> TodoTitle:
        """Return the todo's title."""
        return self._title

    @property
    def description(self) -> Optional[TodoDescription]:
        """Return the todo's description if available."""
        return self._description

    @property
    def status(self) -> TodoStatus:
        """Return the todo's current status."""
        return self._status

    @property
    def created_at(self) -> datetime:
        """Return the todo's creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Return the todo's last update timestamp."""
        return self._updated_at

    @property
    def completed_at(self) -> Optional[datetime]:
        """Return the todo's completion timestamp if set."""
        return self._completed_at

    def update_title(self, new_title: TodoTitle) -> None:
        """Update the todo title and refresh timestamps.

        Args:
            new_title: Replacement title for the todo.
        """
        self._title = new_title
        self._updated_at = datetime.now()

    def update_description(self, new_description: Optional[TodoDescription]) -> None:
        """Update the todo description and refresh timestamps.

        Args:
            new_description: Optional replacement description.
        """
        self._description = new_description if new_description else None
        self._updated_at = datetime.now()

    def start(self) -> None:
        """Mark the todo as in progress and update timestamps."""
        self._status = TodoStatus.IN_PROGRESS
        self._updated_at = datetime.now()

    def complete(self) -> None:
        """Mark the todo as completed and record completion time.

        Raises:
            ValueError: If the todo is already completed.
        """
        if self._status == TodoStatus.COMPLETED:
            raise ValueError('Already completed')

        self._status = TodoStatus.COMPLETED
        self._completed_at = datetime.now()
        self._updated_at = self._completed_at

    @property
    def is_completed(self) -> bool:
        """Return whether the todo is marked as completed."""
        return self._status == TodoStatus.COMPLETED

    def is_overdue(
        self, deadline: datetime, current_time: Optional[datetime] = None
    ) -> bool:
        """Determine whether the todo has passed the provided deadline.

        Args:
            deadline: Deadline timestamp used for comparison.
            current_time: Current timestamp to compare against the deadline.

        Returns:
            bool: True when the todo is incomplete and past the deadline; otherwise False.
        """
        if self.is_completed:
            return False
        return (current_time or datetime.now()) > deadline

    @staticmethod
    def create(
        title: TodoTitle, description: Optional[TodoDescription] = None
    ) -> 'Todo':
        """Create a new todo entity with generated identifier.

        Args:
            title: Title describing the todo to create.
            description: Optional description for the todo.

        Returns:
            Todo: Newly created todo instance.
        """
        return Todo(TodoId.generate(), title, description)
