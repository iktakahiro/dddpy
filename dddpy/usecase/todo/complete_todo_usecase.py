"""This module provides use case for completing a Todo entity."""

from abc import ABC, abstractmethod

from dddpy.domain.todo import (
    TodoAlreadyCompletedError,
    TodoId,
    TodoNotFoundError,
    TodoNotStartedError,
    TodoRepository,
    TodoStatus,
)


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
    return CompleteTodoUseCaseImpl(todo_repository)
