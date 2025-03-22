"""Repository interface for ToDo entities."""

from typing import List, Optional

from dddpy.domain.todo.todo import ToDo, ToDoId


class ToDoRepository:
    """Interface for ToDo repository"""

    def save(self, todo: ToDo) -> None:
        """Save a ToDo"""
        raise NotImplementedError

    def find_by_id(self, todo_id: ToDoId) -> Optional[ToDo]:
        """Find a ToDo by ID"""
        raise NotImplementedError

    def find_all(self) -> List[ToDo]:
        """Get all ToDos"""
        raise NotImplementedError

    def delete(self, todo_id: ToDoId) -> None:
        """Delete a ToDo by ID"""
        raise NotImplementedError
