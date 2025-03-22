"""SQLite implementation of Todo repository."""

from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from dddpy.domain.todo import Todo, TodoId, TodoRepository
from dddpy.infrastructure.sqlite.todo import TodoDTO


class TodoRepositoryImpl(TodoRepository):
    """SQLite implementation of Todo repository interface."""

    def __init__(self, session: Session):
        """Initialize repository with SQLAlchemy session."""
        self.session = session

    def find_by_id(self, todo_id: TodoId) -> Optional[Todo]:
        """Find a Todo by its ID."""
        try:
            row = self.session.query(TodoDTO).filter_by(id=todo_id).one()
        except NoResultFound:
            return None

        return row.to_entity()

    def find_all(self) -> List[Todo]:
        """Retrieve all Todo items."""
        rows = self.session.query(TodoDTO).all()
        return [todo_dto.to_entity() for todo_dto in rows]

    def save(self, todo: Todo) -> None:
        """Save a new Todo item."""
        todo_dto = TodoDTO.from_entity(todo)
        self.session.add(todo_dto)

    def update(self, todo: Todo) -> None:
        """Update an existing Todo item."""
        todo_dto = TodoDTO.from_entity(todo)
        row = self.session.query(TodoDTO).filter_by(id=todo_dto.id).one()
        row.title = todo_dto.title
        row.description = todo_dto.description
        row.status = todo_dto.status
        row.updated_at = todo_dto.updated_at
        row.completed_at = todo_dto.completed_at

    def delete(self, todo_id: TodoId) -> None:
        """Delete a Todo item by its ID."""
        self.session.query(TodoDTO).filter_by(id=todo_id).delete()
