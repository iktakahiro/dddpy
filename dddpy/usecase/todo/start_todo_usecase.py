"""This module provides use case for starting a Todo entity."""

from abc import ABC, abstractmethod

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.exceptions import (
    TodoAlreadyCompletedError,
    TodoAlreadyStartedError,
    TodoNotFoundError,
)
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoId, TodoStatus


class StartTodoUseCase(ABC):
    """StartTodoUseCase defines an interface for starting a Todo."""

    @abstractmethod
    def execute(self, todo_id: TodoId) -> Todo:
        """execute starts a Todo."""


class StartTodoUseCaseImpl(StartTodoUseCase):
    """StartTodoUseCaseImpl implements the use case for starting a Todo."""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self, todo_id: TodoId) -> Todo:
        """execute starts a Todo."""
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
    """Create a new instance of StartTodoUseCase."""
    return StartTodoUseCaseImpl(todo_repository)
