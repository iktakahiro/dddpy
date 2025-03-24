"""This module provides use case for completing a Todo entity."""

from abc import ABC, abstractmethod

from dddpy.domain.todo.exceptions import (
    TodoAlreadyCompletedError,
    TodoNotFoundError,
    TodoNotStartedError,
)
from dddpy.domain.todo.repositories.todo_repository import TodoRepository
from dddpy.domain.todo.value_objects import TodoId, TodoStatus


class CompleteTodoUseCase(ABC):
    """CompleteTodoUseCase defines an interface for completing a Todo."""

    @abstractmethod
    def execute(self, todo_id: TodoId) -> None:
        """execute completes a Todo."""


class CompleteTodoUseCaseImpl(CompleteTodoUseCase):
    """CompleteTodoUseCaseImpl implements the use case for completing a Todo."""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self, todo_id: TodoId) -> None:
        """execute completes a Todo."""
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        if todo.status == TodoStatus.NOT_STARTED:
            raise TodoNotStartedError

        if todo.is_completed:
            raise TodoAlreadyCompletedError

        todo.complete()
        self.todo_repository.save(todo)


def new_complete_todo_usecase(todo_repository: TodoRepository) -> CompleteTodoUseCase:
    """Create a new instance of CompleteTodoUseCase."""
    return CompleteTodoUseCaseImpl(todo_repository)
