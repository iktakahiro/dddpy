"""This module provides use cases for querying ToDo entities."""

from abc import abstractmethod
from typing import List, Optional

from dddpy.domain.todo import ToDo, ToDoId, ToDoNotFoundError, ToDoRepository


class ToDoQueryUseCase:
    """ToDoQueryUseCase defines a query use cases interface related ToDo entity."""

    @abstractmethod
    def fetch_todo_by_id(self, todo_id: ToDoId) -> Optional[ToDo]:
        """Fetch a ToDo by its ID."""
        raise NotImplementedError

    @abstractmethod
    def fetch_todos(self) -> List[ToDo]:
        """Fetch all ToDos."""
        raise NotImplementedError


class ToDoQueryUseCaseImpl(ToDoQueryUseCase):
    """ToDoQueryUseCaseImpl implements a query use cases related ToDo entity."""

    def __init__(self, todo_repository: ToDoRepository):
        self.todo_repository = todo_repository

    def fetch_todo_by_id(self, todo_id: ToDoId) -> Optional[ToDo]:
        """fetch_todo_by_id fetches a ToDo by ID."""
        todo = self.todo_repository.find_by_id(todo_id)
        if todo is None:
            raise ToDoNotFoundError
        return todo

    def fetch_todos(self) -> List[ToDo]:
        """fetch_todos fetches all ToDos."""
        return self.todo_repository.find_all()
