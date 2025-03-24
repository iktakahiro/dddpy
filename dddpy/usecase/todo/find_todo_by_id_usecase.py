"""This module provides use case for finding a Todo entity by its ID."""

from abc import ABC, abstractmethod

from dddpy.domain.todo import Todo, TodoId, TodoNotFoundError, TodoRepository


class FindTodoByIdUseCase(ABC):
    """FindTodoByIdUseCase defines a use case interface for finding a Todo by its ID."""

    @abstractmethod
    def execute(self, todo_id: TodoId) -> Todo:
        """execute finds a Todo by its ID."""


class FindTodoByIdUseCaseImpl(FindTodoByIdUseCase):
    """FindTodoByIdUseCaseImpl implements the use case for finding a Todo by its ID."""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self, todo_id: TodoId) -> Todo:
        """execute finds a Todo by its ID."""
        todo = self.todo_repository.find_by_id(todo_id)
        if todo is None:
            raise TodoNotFoundError
        return todo


def new_find_todo_by_id_usecase(todo_repository: TodoRepository) -> FindTodoByIdUseCase:
    """Create a new instance of FindTodoByIdUseCase."""
    return FindTodoByIdUseCaseImpl(todo_repository)
