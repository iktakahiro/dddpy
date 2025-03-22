"""Repository interface for Todo entities."""

from typing import List, Optional

from dddpy.domain.todo import Todo, TodoId


class TodoRepository:
    """Interface for Todo repository"""

    def save(self, todo: Todo) -> None:
        """Save a Todo"""
        raise NotImplementedError

    def find_by_id(self, todo_id: TodoId) -> Optional[Todo]:
        """Find a Todo by ID"""
        raise NotImplementedError

    def find_all(self) -> List[Todo]:
        """Get all Todos"""
        raise NotImplementedError

    def delete(self, todo_id: TodoId) -> None:
        """Delete a Todo by ID"""
        raise NotImplementedError
