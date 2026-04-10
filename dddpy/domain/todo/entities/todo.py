"""Define the Todo entity used throughout the domain layer."""

from dataclasses import dataclass, field
from datetime import datetime

from dddpy.domain.todo.value_objects import (
    TodoDescription,
    TodoId,
    TodoStatus,
    TodoTitle,
)

ALREADY_COMPLETED_ERROR_MESSAGE = 'Already completed'


@dataclass(eq=False)
class Todo:
    """Represent a todo item tracked by the domain.

    Attributes:
        id: Unique identifier for the todo.
        title: Title describing the todo.
        description: Optional detailed description.
        status: Current lifecycle status.
        created_at: Timestamp when the todo was created.
        updated_at: Timestamp when the todo was last updated.
        completed_at: Optional timestamp when the todo was completed.
    """

    id: TodoId
    title: TodoTitle
    description: TodoDescription | None = None
    status: TodoStatus = TodoStatus.NOT_STARTED
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None

    def __hash__(self) -> int:
        """Return a hash value based on the entity identity."""
        return hash(self.id)

    def __eq__(self, obj: object) -> bool:
        """Compare todos by identifier."""
        if isinstance(obj, Todo):
            return self.id == obj.id

        return False

    def update_title(self, new_title: TodoTitle) -> None:
        """Update the todo title and refresh timestamps.

        Args:
            new_title: Replacement title for the todo.
        """
        self.title = new_title
        self.updated_at = datetime.now()

    def update_description(self, new_description: TodoDescription | None) -> None:
        """Update the todo description and refresh timestamps.

        Args:
            new_description: Optional replacement description.
        """
        self.description = new_description if new_description else None
        self.updated_at = datetime.now()

    def start(self) -> None:
        """Mark the todo as in progress and update timestamps."""
        self.status = TodoStatus.IN_PROGRESS
        self.updated_at = datetime.now()

    def complete(self) -> None:
        """Mark the todo as completed and record completion time.

        Raises:
            ValueError: If the todo is already completed.
        """
        if self.status == TodoStatus.COMPLETED:
            raise ValueError(ALREADY_COMPLETED_ERROR_MESSAGE)

        self.status = TodoStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = self.completed_at

    @property
    def is_completed(self) -> bool:
        """Return whether the todo is marked as completed."""
        return self.status == TodoStatus.COMPLETED

    def is_overdue(
        self, deadline: datetime, current_time: datetime | None = None
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
    def create(title: TodoTitle, description: TodoDescription | None = None) -> 'Todo':
        """Create a new todo entity with generated identifier.

        Args:
            title: Title describing the todo to create.
            description: Optional description for the todo.

        Returns:
            Todo: Newly created todo instance.
        """
        return Todo(TodoId.generate(), title, description)
