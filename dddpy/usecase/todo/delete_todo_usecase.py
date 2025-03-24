"""This module provides use case for deleting a Todo entity."""

from abc import ABC, abstractmethod

from dddpy.domain.todo import TodoId, TodoNotFoundError, TodoRepository


class DeleteTodoUseCase(ABC):
    """DeleteTodoUseCase defines an interface for deleting a Todo."""

    @abstractmethod
    def execute(self, todo_id: TodoId) -> None:
        """execute deletes a Todo by its ID."""


class DeleteTodoUseCaseImpl(DeleteTodoUseCase):
    """DeleteTodoUseCaseImpl implements the use case for deleting a Todo."""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self, todo_id: TodoId) -> None:
        """execute deletes a Todo by its ID."""
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        self.todo_repository.delete(todo_id)


def new_delete_todo_usecase(todo_repository: TodoRepository) -> DeleteTodoUseCase:
    """Create a new instance of DeleteTodoUseCase."""
    return DeleteTodoUseCaseImpl(todo_repository)
