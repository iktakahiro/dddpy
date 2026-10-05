"""Provide use case implementations for deleting todos."""

from typing import Protocol, override

from dddpy.domain.todo.exceptions import TodoNotFoundError
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoId


class DeleteTodoUseCase(Protocol):
    """Define the application boundary for deleting todos."""

    def execute(self, todo_id: TodoId) -> None:
        """Delete a todo identified by the provided ID.

        Args:
            todo_id: Identifier of the todo to delete.
        """


class DeleteTodoUseCaseImpl(DeleteTodoUseCase):
    """Concrete todo deletion use case backed by a repository."""

    def __init__(self, todo_repository: TodoRepository):
        """Store the repository dependency.

        Args:
            todo_repository: Repository responsible for todo persistence.
        """
        self.todo_repository = todo_repository

    @override
    def execute(self, todo_id: TodoId) -> None:
        """Delete a todo after ensuring it exists.

        Args:
            todo_id: Identifier of the todo to delete.

        Raises:
            TodoNotFoundError: If no todo matches the provided identifier.
        """
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        self.todo_repository.delete(todo_id)


def new_delete_todo_usecase(todo_repository: TodoRepository) -> DeleteTodoUseCase:
    """Instantiate the todo deletion use case.

    Args:
        todo_repository: Repository responsible for todo persistence.

    Returns:
        DeleteTodoUseCase: Configured use case implementation.
    """
    return DeleteTodoUseCaseImpl(todo_repository)
