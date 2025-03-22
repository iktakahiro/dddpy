"""This module provides use cases for command operations related to ToDo entities."""

from abc import abstractmethod
from typing import Optional

from dddpy.domain.todo import (
    ToDo,
    ToDoAlreadyCompletedError,
    ToDoAlreadyStartedError,
    ToDoDescription,
    ToDoId,
    ToDoNotFoundError,
    ToDoNotStartedError,
    ToDoRepository,
    ToDoStatus,
    ToDoTitle,
)


class ToDoCommandUseCase:
    """ToDoCommandUseCase defines a command use case interface related ToDo entity."""

    @abstractmethod
    def create_todo(self, title: ToDoTitle, description: ToDoDescription) -> None:
        """Create a new ToDo."""
        raise NotImplementedError

    @abstractmethod
    def start_todo(self, todo_id: ToDoId) -> None:
        """Start a ToDo."""
        raise NotImplementedError

    @abstractmethod
    def complete_todo(self, todo_id: ToDoId) -> None:
        """Complete a ToDo."""
        raise NotImplementedError

    @abstractmethod
    def update_todo(
        self, todo_id: ToDoId, title: ToDoTitle, description: ToDoDescription
    ) -> None:
        """Update a ToDo."""
        raise NotImplementedError

    @abstractmethod
    def delete_todo(self, todo_id: ToDoId) -> None:
        """Delete a ToDo by its ID."""
        raise NotImplementedError


class ToDoCommandUseCaseImpl(ToDoCommandUseCase):
    """ToDoCommandUseCaseImpl implements a command use cases related ToDo entity."""

    def __init__(self, todo_repository: ToDoRepository):
        self.todo_repository = todo_repository

    def create_todo(self, title: ToDoTitle, description: ToDoDescription) -> None:
        """create_todo creates a new ToDo."""
        todo = ToDo.create(title=title, description=description)
        self.todo_repository.save(todo)

    def start_todo(self, todo_id: ToDoId) -> None:
        """start_todo starts a ToDo."""
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise ToDoNotFoundError

        if todo.is_completed:
            raise ToDoAlreadyCompletedError

        if todo.status == ToDoStatus.IN_PROGRESS:
            raise ToDoAlreadyStartedError

        todo.start()

        self.todo_repository.save(todo)

    def complete_todo(self, todo_id: ToDoId) -> None:
        """complete_todo completes a ToDo."""
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise ToDoNotFoundError

        if todo.status == ToDoStatus.NOT_STARTED:
            raise ToDoNotStartedError

        if todo.is_completed:
            raise ToDoAlreadyCompletedError

        todo.complete()

        self.todo_repository.save(todo)

    def update_todo(
        self, todo_id: ToDoId, title: ToDoTitle, description: Optional[ToDoDescription]
    ) -> None:
        """update_todo updates a ToDo."""
        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise ToDoNotFoundError

        todo.update_title(title)
        todo.update_description(description)

        self.todo_repository.save(todo)

    def delete_todo(self, todo_id: ToDoId) -> None:
        """delete_todo deletes a ToDo by its ID."""

        todo = self.todo_repository.find_by_id(todo_id)

        if todo is None:
            raise ToDoNotFoundError

        self.todo_repository.delete(todo_id)
