"""Repository interface for Todo entities."""

from abc import ABC, abstractmethod
from typing import List, Optional

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.value_objects import TodoId


class TodoRepository(ABC):
    """Interface for Todo repository"""

    @abstractmethod
    def save(self, todo: Todo) -> None:
        """Save a Todo"""

    @abstractmethod
    def find_by_id(self, todo_id: TodoId) -> Optional[Todo]:
        """Find a Todo by ID"""

    @abstractmethod
    def find_all(self) -> List[Todo]:
        """Get all Todos"""

    @abstractmethod
    def delete(self, todo_id: TodoId) -> None:
        """Delete a Todo by ID"""
