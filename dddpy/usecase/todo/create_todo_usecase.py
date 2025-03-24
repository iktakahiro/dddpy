"""This module provides use case for creating a new Todo entity."""

from abc import abstractmethod
from typing import Optional

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.repositories.todo_repository import TodoRepository
from dddpy.domain.todo.value_objects import TodoDescription, TodoTitle


class CreateTodoUseCase:
    """CreateTodoUseCase defines a use case interface for creating a new Todo."""

    @abstractmethod
    def execute(
        self, title: TodoTitle, description: Optional[TodoDescription] = None
    ) -> Todo:
        """execute creates a new Todo."""


class CreateTodoUseCaseImpl(CreateTodoUseCase):
    """CreateTodoUseCaseImpl implements the use case for creating a new Todo."""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(
        self, title: TodoTitle, description: Optional[TodoDescription] = None
    ) -> Todo:
        """execute creates a new Todo."""
        todo = Todo.create(title=title, description=description)
        self.todo_repository.save(todo)
        return todo


def new_create_todo_usecase(todo_repository: TodoRepository) -> CreateTodoUseCase:
    """Create a new instance of CreateTodoUseCase."""
    return CreateTodoUseCaseImpl(todo_repository)
