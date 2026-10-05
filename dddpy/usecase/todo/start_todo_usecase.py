"""Provide use case implementations for starting todos."""

from typing import Protocol, override

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.exceptions import (
    TodoAlreadyCompletedError,
    TodoAlreadyStartedError,
    TodoNotFoundError,
)
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoId, TodoStatus


class StartTodoUseCase(Protocol):
    """Define the application boundary for starting todos."""

    def execute(self, todo_id: TodoId) -> Todo:
        """Start a todo identified by the provided ID.

        Args:
            todo_id: Identifier of the todo to start.

        Returns:
            Todo: Updated todo entity in progress.
        """


class StartTodoUseCaseImpl(StartTodoUseCase):
    """Concrete todo start use case backed by a repository."""

    def __init__(self, todo_repository: TodoRepository):
        """Store the repository dependency.

        Args:
            todo_repository: Repository used to persist todo updates.
        """
        self.todo_repository = todo_repository

    @override
    def execute(self, todo_id: TodoId) -> Todo:
        """Start a todo after validating its current lifecycle state.

        Args:
            todo_id: Identifier of the todo to start.

        Raises:
            TodoNotFoundError: If the todo cannot be located.
            TodoAlreadyCompletedError: If the todo is already completed.
            TodoAlreadyStartedError: If the todo is already in progress.

        Returns:
            Todo: Persisted todo marked as in progress.
        """
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        if todo.is_completed:
            raise TodoAlreadyCompletedError

        if todo.status == TodoStatus.IN_PROGRESS:
            raise TodoAlreadyStartedError

        todo.start()
        self.todo_repository.save(todo)
        return todo


def new_start_todo_usecase(todo_repository: TodoRepository) -> StartTodoUseCase:
    """Instantiate the todo start use case.

    Args:
        todo_repository: Repository used to persist todo updates.

    Returns:
        StartTodoUseCase: Configured use case implementation.
    """
    return StartTodoUseCaseImpl(todo_repository)
