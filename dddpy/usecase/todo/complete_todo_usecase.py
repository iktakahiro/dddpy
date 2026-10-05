"""Provide use case implementations for completing todos."""

from typing import Protocol, override

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.exceptions import (
    TodoAlreadyCompletedError,
    TodoNotFoundError,
    TodoNotStartedError,
)
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoId, TodoStatus


class CompleteTodoUseCase(Protocol):
    """Define the application boundary for completing todos."""

    def execute(self, todo_id: TodoId) -> Todo:
        """Complete a todo identified by the provided ID.

        Args:
            todo_id: Identifier of the todo to complete.

        Returns:
            Todo: Updated todo entity marked as completed.
        """


class CompleteTodoUseCaseImpl(CompleteTodoUseCase):
    """Concrete todo completion use case backed by a repository."""

    def __init__(self, todo_repository: TodoRepository):
        """Store the repository dependency.

        Args:
            todo_repository: Repository used to persist todo updates.
        """
        self.todo_repository = todo_repository

    @override
    def execute(self, todo_id: TodoId) -> Todo:
        """Complete a todo after validating its lifecycle state.

        Args:
            todo_id: Identifier of the todo to complete.

        Raises:
            TodoNotFoundError: If the todo cannot be located.
            TodoNotStartedError: If the todo has not been started yet.
            TodoAlreadyCompletedError: If the todo is already completed.

        Returns:
            Todo: Persisted todo marked as completed.
        """
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        if todo.status == TodoStatus.NOT_STARTED:
            raise TodoNotStartedError

        if todo.is_completed:
            raise TodoAlreadyCompletedError

        todo.complete()
        self.todo_repository.save(todo)
        return todo


def new_complete_todo_usecase(todo_repository: TodoRepository) -> CompleteTodoUseCase:
    """Instantiate the todo completion use case.

    Args:
        todo_repository: Repository used to persist todo updates.

    Returns:
        CompleteTodoUseCase: Configured use case implementation.
    """
    return CompleteTodoUseCaseImpl(todo_repository)
