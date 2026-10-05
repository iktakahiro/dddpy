"""Provide use case implementations for retrieving todos by ID."""

from typing import Protocol, override

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.exceptions import TodoNotFoundError
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoId


class FindTodoByIdUseCase(Protocol):
    """Define the application boundary for retrieving a todo by ID."""

    def execute(self, todo_id: TodoId) -> Todo:
        """Return the todo matching the provided identifier.

        Args:
            todo_id: Identifier of the todo to retrieve.

        Returns:
            Todo: Todo entity matching the identifier.
        """


class FindTodoByIdUseCaseImpl(FindTodoByIdUseCase):
    """Concrete todo lookup use case backed by a repository."""

    def __init__(self, todo_repository: TodoRepository):
        """Store the repository dependency.

        Args:
            todo_repository: Repository used to retrieve todos.
        """
        self.todo_repository = todo_repository

    @override
    def execute(self, todo_id: TodoId) -> Todo:
        """Retrieve a todo by identifier or raise if absent.

        Args:
            todo_id: Identifier of the todo to retrieve.

        Raises:
            TodoNotFoundError: If the todo cannot be located.

        Returns:
            Todo: Matching todo entity.
        """
        todo = self.todo_repository.find_by_id(todo_id)
        if todo is None:
            raise TodoNotFoundError
        return todo


def new_find_todo_by_id_usecase(todo_repository: TodoRepository) -> FindTodoByIdUseCase:
    """Instantiate the todo lookup by ID use case.

    Args:
        todo_repository: Repository used to retrieve todos.

    Returns:
        FindTodoByIdUseCase: Configured use case implementation.
    """
    return FindTodoByIdUseCaseImpl(todo_repository)
