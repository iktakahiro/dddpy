"""SQLite implementation of Todo repository."""

from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.repositories.todo_repository import TodoRepository
from dddpy.domain.todo.value_objects import TodoId
from dddpy.infrastructure.sqlite.todo import TodoDTO


class TodoRepositoryImpl(TodoRepository):
    """SQLite implementation of Todo repository interface."""

    def __init__(self, session: Session):
        """Initialize repository with SQLAlchemy session."""
        self.session = session

    def find_by_id(self, todo_id: TodoId) -> Optional[Todo]:
        """Find a Todo by its ID."""
        try:
            row = self.session.query(TodoDTO).filter_by(id=todo_id.value).one()
        except NoResultFound:
            return None

        return row.to_entity()

    def find_all(self) -> List[Todo]:
        """Retrieve all Todo items."""
        rows = (
            self.session.query(TodoDTO)
            .order_by(desc(TodoDTO.created_at))
            .limit(20)
            .all()
        )
        return [todo_dto.to_entity() for todo_dto in rows]

    def save(self, todo: Todo) -> None:
        """Save a new Todo item."""
        todo_dto = TodoDTO.from_entity(todo)
        try:
            existing_todo = (
                self.session.query(TodoDTO).filter_by(id=todo.id.value).one()
            )
        except NoResultFound:
            self.session.add(todo_dto)

        else:
            existing_todo.title = todo_dto.title
            existing_todo.description = todo_dto.description
            existing_todo.status = todo_dto.status
            existing_todo.updated_at = todo_dto.updated_at
            existing_todo.completed_at = todo_dto.completed_at

    def delete(self, todo_id: TodoId) -> None:
        """Delete a Todo item by its ID."""
        self.session.query(TodoDTO).filter_by(id=todo_id.value).delete()


def new_todo_repository(session: Session) -> TodoRepository:
    """Create a new TodoRepository instance."""
    return TodoRepositoryImpl(session)
