"""This module provides use cases for querying Todo entities."""

from abc import abstractmethod
from typing import List, Optional

from dddpy.domain.todo import Todo, TodoId, TodoNotFoundError, TodoRepository


class TodoQueryUseCase:
    """TodoQueryUseCase defines a query use cases interface related Todo entity."""

    @abstractmethod
    def fetch_todo_by_id(self, todo_id: TodoId) -> Todo:
        """Fetch a Todo by its ID."""
        raise NotImplementedError

    @abstractmethod
    def fetch_todos(self) -> List[Todo]:
        """Fetch all Todos."""
        raise NotImplementedError


class TodoQueryUseCaseImpl(TodoQueryUseCase):
    """TodoQueryUseCaseImpl implements a query use cases related Todo entity."""

    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def fetch_todo_by_id(self, todo_id: TodoId) -> Todo:
        """fetch_todo_by_id fetches a Todo by ID."""
        todo = self.todo_repository.find_by_id(todo_id)
        if todo is None:
            raise TodoNotFoundError
        return todo

    def fetch_todos(self) -> List[Todo]:
        """fetch_todos fetches all Todos."""
        return self.todo_repository.find_all()
