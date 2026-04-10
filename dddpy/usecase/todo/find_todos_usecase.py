"""Provide use case implementations for listing todos."""

from abc import ABC, abstractmethod

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.repositories import TodoRepository


class FindTodosUseCase(ABC):
    """Define the application boundary for listing todos."""

    @abstractmethod
    def execute(self) -> list[Todo]:
        """Return the collection of todos managed by the system.

        Returns:
            List[Todo]: All persisted todo entities.
        """


class FindTodosUseCaseImpl(FindTodosUseCase):
    """Concrete todo listing use case backed by a repository."""

    def __init__(self, todo_repository: TodoRepository):
        """Store the repository dependency.

        Args:
            todo_repository: Repository used to retrieve todos.
        """
        self.todo_repository = todo_repository

    def execute(self) -> list[Todo]:
        """Return all todos ordered per repository implementation."""
        return self.todo_repository.find_all()


def new_find_todos_usecase(todo_repository: TodoRepository) -> FindTodosUseCase:
    """Instantiate the todo listing use case.

    Args:
        todo_repository: Repository used to retrieve todos.

    Returns:
        FindTodosUseCase: Configured use case implementation.
    """
    return FindTodosUseCaseImpl(todo_repository)
