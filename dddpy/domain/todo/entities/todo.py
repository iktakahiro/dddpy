"""Define the Todo entity used throughout the domain layer."""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from dddpy.domain.todo.exceptions import (
    TodoAlreadyCompletedError,
    TodoAlreadyStartedError,
    TodoNotStartedError,
)
from dddpy.domain.todo.value_objects import (
    TodoDescription,
    TodoId,
    TodoStatus,
    TodoTitle,
)

# No longer raised by Todo.complete(), which now raises TodoAlreadyCompletedError.
# Kept only for backward compatibility with existing external imports.
ALREADY_COMPLETED_ERROR_MESSAGE = 'Already completed'


def _now() -> datetime:
    """Return the current time in UTC."""
    return datetime.now(UTC)


def _to_utc(value: datetime) -> datetime:
    """Return an aware datetime, reading naive values as server local time.

    This matches the persistence layer, which converts naive datetimes with
    ``datetime.timestamp()``. Aware values are returned unchanged.
    """
    if value.utcoffset() is None:
        return value.astimezone(UTC)
    return value


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

    Naive ``created_at``, ``updated_at`` and ``completed_at`` values are
    interpreted as server local time and normalized to aware UTC datetimes.
    Aware values keep their instant.
    """

    id: TodoId
    title: TodoTitle
    description: TodoDescription | None = None
    status: TodoStatus = TodoStatus.NOT_STARTED
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        """Normalize naive timestamps so values are never a mix of naive and aware."""
        self.created_at = _to_utc(self.created_at)
        self.updated_at = _to_utc(self.updated_at)
        if self.completed_at is not None:
            self.completed_at = _to_utc(self.completed_at)

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
        self.updated_at = _now()

    def update_description(self, new_description: TodoDescription | None) -> None:
        """Update the todo description and refresh timestamps.

        Args:
            new_description: Optional replacement description.
        """
        self.description = new_description if new_description else None
        self.updated_at = _now()

    def start(self) -> None:
        """Mark the todo as in progress and update timestamps.

        Raises:
            TodoAlreadyCompletedError: If the todo is already completed.
            TodoAlreadyStartedError: If the todo is already in progress.
        """
        if self.status == TodoStatus.COMPLETED:
            raise TodoAlreadyCompletedError

        if self.status == TodoStatus.IN_PROGRESS:
            raise TodoAlreadyStartedError

        self.status = TodoStatus.IN_PROGRESS
        self.updated_at = _now()

    def complete(self) -> None:
        """Mark the todo as completed and record completion time.

        Raises:
            TodoNotStartedError: If the todo has not been started yet.
            TodoAlreadyCompletedError: If the todo is already completed.
        """
        if self.status == TodoStatus.NOT_STARTED:
            raise TodoNotStartedError

        if self.status == TodoStatus.COMPLETED:
            raise TodoAlreadyCompletedError

        self.status = TodoStatus.COMPLETED
        self.completed_at = _now()
        self.updated_at = self.completed_at

    @property
    def is_completed(self) -> bool:
        """Return whether the todo is marked as completed."""
        return self.status == TodoStatus.COMPLETED

    def is_overdue(
        self, deadline: datetime, current_time: datetime | None = None
    ) -> bool:
        """Determine whether the todo has passed the provided deadline.

        Naive deadline and current-time inputs are interpreted as server local
        time and converted to UTC. Aware inputs keep their instant.

        Args:
            deadline: Deadline timestamp used for comparison.
            current_time: Current timestamp to compare against the deadline.

        Returns:
            bool: True when the todo is incomplete and past the deadline; otherwise False.
        """
        if self.is_completed:
            return False
        now = _to_utc(current_time) if current_time is not None else _now()
        return now > _to_utc(deadline)

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
