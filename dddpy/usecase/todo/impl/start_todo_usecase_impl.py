"""This module provides implementation for starting a Todo entity."""

from dddpy.domain.todo import (
    TodoAlreadyCompletedError,
    TodoAlreadyStartedError,
    TodoId,
    TodoNotFoundError,
    TodoRepository,
    TodoStatus,
)
from dddpy.usecase.todo.start_todo_usecase import StartTodoUseCase


class StartTodoUseCaseImpl(StartTodoUseCase):
    """StartTodoUseCaseImpl implements the use case for starting a Todo."""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self, todo_id: TodoId) -> None:
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
