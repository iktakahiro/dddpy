"""This module provides use case for updating a Todo entity."""

from abc import ABC, abstractmethod
from typing import Optional

from dddpy.domain.todo import (
    TodoDescription,
    TodoId,
    TodoNotFoundError,
    TodoRepository,
    TodoTitle,
)


class UpdateTodoUseCase(ABC):
    """UpdateTodoUseCase defines an interface for updating a Todo."""

    @abstractmethod
    def execute(
        self, todo_id: TodoId, title: TodoTitle, description: Optional[TodoDescription]
    ) -> None:
        """execute updates a Todo."""
        pass


class UpdateTodoUseCaseImpl(UpdateTodoUseCase):
    """UpdateTodoUseCaseImpl implements the use case for updating a Todo."""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(
        self, todo_id: TodoId, title: TodoTitle, description: Optional[TodoDescription]
    ) -> None:
        """execute updates a Todo."""
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        todo.update_title(title)
        todo.update_description(description)
        self.todo_repository.save(todo)


def new_update_todo_usecase(todo_repository: TodoRepository) -> UpdateTodoUseCase:
    return UpdateTodoUseCaseImpl(todo_repository)
