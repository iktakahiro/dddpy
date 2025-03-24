"""This module provides use case for finding all Todo entities."""

from abc import ABC, abstractmethod
from typing import List

from dddpy.domain.todo import Todo, TodoRepository


class FindTodosUseCase(ABC):
    """FindTodosUseCase defines a use case interface for finding all Todos."""

    @abstractmethod
    def execute(self) -> List[Todo]:
        """execute finds all Todos."""


class FindTodosUseCaseImpl(FindTodosUseCase):
    """FindTodosUseCaseImpl implements the use case for finding all Todos."""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self) -> List[Todo]:
        """execute finds all Todos."""
        return self.todo_repository.find_all()


def new_find_todos_usecase(todo_repository: TodoRepository) -> FindTodosUseCase:
    """Create a new instance of FindTodosUseCase."""
    return FindTodosUseCaseImpl(todo_repository)
