"""This module provides use cases for command operations related to Todo entities."""

from abc import abstractmethod
from typing import Optional

from dddpy.domain.todo import (
    Todo,
    TodoAlreadyCompletedError,
    TodoAlreadyStartedError,
    TodoDescription,
    TodoId,
    TodoNotFoundError,
    TodoNotStartedError,
    TodoRepository,
    TodoStatus,
    TodoTitle,
)


class TodoCommandUseCase:
    """TodoCommandUseCase defines a command use case interface related Todo entity."""

    @abstractmethod
    def create_todo(
        self, title: TodoTitle, description: Optional[TodoDescription] = None
    ) -> Todo:
        """Create a new Todo."""
        raise NotImplementedError

    @abstractmethod
    def start_todo(self, todo_id: TodoId) -> None:
        """Start a Todo."""
        raise NotImplementedError

    @abstractmethod
    def complete_todo(self, todo_id: TodoId) -> None:
        """Complete a Todo."""
        raise NotImplementedError

    @abstractmethod
    def update_todo(
        self, todo_id: TodoId, title: TodoTitle, description: Optional[TodoDescription]
    ) -> None:
        """Update a Todo."""
        raise NotImplementedError

    @abstractmethod
    def delete_todo(self, todo_id: TodoId) -> None:
        """Delete a Todo by its ID."""
        raise NotImplementedError


class TodoCommandUseCaseImpl(TodoCommandUseCase):
    """TodoCommandUseCaseImpl implements a command use cases related Todo entity."""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def create_todo(
        self, title: TodoTitle, description: Optional[TodoDescription] = None
    ) -> Todo:
        """create_todo creates a new Todo."""
        todo = Todo.create(title=title, description=description)
        self.todo_repository.save(todo)
        return todo

    def start_todo(self, todo_id: TodoId) -> None:
        """start_todo starts a Todo."""
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        if todo.is_completed:
            raise TodoAlreadyCompletedError

        if todo.status == TodoStatus.IN_PROGRESS:
            raise TodoAlreadyStartedError

        todo.start()

        self.todo_repository.save(todo)

    def complete_todo(self, todo_id: TodoId) -> None:
        """complete_todo completes a Todo."""
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        if todo.status == TodoStatus.NOT_STARTED:
            raise TodoNotStartedError

        if todo.is_completed:
            raise TodoAlreadyCompletedError

        todo.complete()

        self.todo_repository.save(todo)

    def update_todo(
        self, todo_id: TodoId, title: TodoTitle, description: Optional[TodoDescription]
    ) -> None:
        """update_todo updates a Todo."""
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        todo.update_title(title)
        todo.update_description(description)

        self.todo_repository.save(todo)

    def delete_todo(self, todo_id: TodoId) -> None:
        """delete_todo deletes a Todo by its ID."""

        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise TodoNotFoundError

        self.todo_repository.delete(todo_id)
