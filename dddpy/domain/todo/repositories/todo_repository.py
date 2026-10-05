"""Define the repository abstraction for todo entities."""

from typing import Protocol

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.value_objects import TodoId


class TodoRepository(Protocol):
    """Provide the abstraction for todo persistence operations."""

    def save(self, todo: Todo) -> None:
        """Persist the provided todo entity.

        Args:
            todo: Todo instance to store or update.
        """

    def find_by_id(self, todo_id: TodoId) -> Todo | None:
        """Retrieve a todo by its identifier.

        Args:
            todo_id: Identifier of the todo to fetch.

        Returns:
            Optional[Todo]: The matching todo when found; otherwise None.
        """

    def find_all(self) -> list[Todo]:
        """Return the collection of todos stored in the repository.

        Returns:
            List[Todo]: All persisted todos.
        """

    def delete(self, todo_id: TodoId) -> None:
        """Remove the todo identified by the provided ID.

        Args:
            todo_id: Identifier of the todo to delete.
        """
