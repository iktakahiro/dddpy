"""Provide use case implementations for creating todos."""

from abc import ABC, abstractmethod

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoDescription, TodoTitle


class CreateTodoUseCase(ABC):
    """Define the application boundary for creating todos."""

    @abstractmethod
    def execute(
        self, title: TodoTitle, description: TodoDescription | None = None
    ) -> Todo:
        """Create a todo using the provided values.

        Args:
            title: Title for the new todo.
            description: Optional descriptive text.

        Returns:
            Todo: Newly created todo entity.
        """


class CreateTodoUseCaseImpl(CreateTodoUseCase):
    """Concrete todo creation use case backed by a repository."""

    def __init__(self, todo_repository: TodoRepository):
        """Store the repository dependency.

        Args:
            todo_repository: Repository used to persist todos.
        """
        self.todo_repository = todo_repository

    def execute(
        self, title: TodoTitle, description: TodoDescription | None = None
    ) -> Todo:
        """Create, persist, and return a new todo entity.

        Args:
            title: Title for the new todo.
            description: Optional descriptive text.

        Returns:
            Todo: Newly created todo entity.
        """
        todo = Todo.create(title=title, description=description)
        self.todo_repository.save(todo)
        return todo


def new_create_todo_usecase(todo_repository: TodoRepository) -> CreateTodoUseCase:
    """Instantiate the todo creation use case.

    Args:
        todo_repository: Repository used to persist new todos.

    Returns:
        CreateTodoUseCase: Configured use case implementation.
    """
    return CreateTodoUseCaseImpl(todo_repository)
