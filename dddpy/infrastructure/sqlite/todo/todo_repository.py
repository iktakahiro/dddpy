"""SQLite implementation of ToDo repository."""

from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from dddpy.domain.todo import ToDo, ToDoId, ToDoRepository
from dddpy.infrastructure.sqlite.todo import ToDoDTO


class ToDoRepositoryImpl(ToDoRepository):
    """SQLite implementation of ToDo repository interface."""

    def __init__(self, session: Session):
        """Initialize repository with SQLAlchemy session."""
        self.session = session

    def find_by_id(self, todo_id: ToDoId) -> Optional[ToDo]:
        """Find a ToDo by its ID."""
        try:
            row = self.session.query(ToDoDTO).filter_by(id=todo_id).one()
        except NoResultFound:
            return None

        return row.to_entity()

    def find_all(self) -> List[ToDo]:
        """Retrieve all ToDo items."""
        rows = self.session.query(ToDoDTO).all()
        return [todo_dto.to_entity() for todo_dto in rows]

    def save(self, todo: ToDo) -> None:
        """Save a new ToDo item."""
        todo_dto = ToDoDTO.from_entity(todo)
        self.session.add(todo_dto)

    def update(self, todo: ToDo) -> None:
        """Update an existing ToDo item."""
        todo_dto = ToDoDTO.from_entity(todo)
        row = self.session.query(ToDoDTO).filter_by(id=todo_dto.id).one()
        row.title = todo_dto.title
        row.description = todo_dto.description
        row.status = todo_dto.status
        row.updated_at = todo_dto.updated_at
        row.completed_at = todo_dto.completed_at

    def delete(self, todo_id: ToDoId) -> None:
        """Delete a ToDo item by its ID."""
        self.session.query(ToDoDTO).filter_by(id=todo_id).delete()
