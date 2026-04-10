"""Provide use case implementations for updating todos."""

from abc import ABC, abstractmethod

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.exceptions import TodoNotFoundError
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoDescription, TodoId, TodoTitle


class UpdateTodoUseCase(ABC):
    """Define the application boundary for updating todos."""

    @abstractmethod
    def execute(
        self,
        todo_id: TodoId,
        title: TodoTitle | None = None,
        description: TodoDescription | None = None,
    ) -> Todo:
        """Update a todo using the provided values.

        Args:
            todo_id: Identifier of the todo to update.
            title: Optional replacement title.
            description: Optional replacement description.

        Returns:
            Todo: Updated todo entity.
        """


class UpdateTodoUseCaseImpl(UpdateTodoUseCase):
    """Concrete todo update use case backed by a repository."""

    def __init__(self, todo_repository: TodoRepository):
        """Store the repository dependency.

        Args:
            todo_repository: Repository used to persist todo updates.
        """
        self.todo_repository = todo_repository

    def execute(
        self,
        todo_id: TodoId,
        title: TodoTitle | None = None,
        description: TodoDescription | None = None,
    ) -> Todo:
        """Update a todo and persist the changes.

        Args:
            todo_id: Identifier of the todo to update.
            title: Optional replacement title.
            description: Optional replacement description.

        Raises:
            TodoNotFoundError: If no todo matches the provided identifier.

        Returns:
            Todo: Persisted todo reflecting the latest updates.
        """
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        if title is not None:
            todo.update_title(title)
        if description is not None:
            todo.update_description(description)

        self.todo_repository.save(todo)
        return todo


def new_update_todo_usecase(todo_repository: TodoRepository) -> UpdateTodoUseCase:
    """Instantiate the todo update use case.

    Args:
        todo_repository: Repository used to persist todo updates.

    Returns:
        UpdateTodoUseCase: Configured use case implementation.
    """
    return UpdateTodoUseCaseImpl(todo_repository)
