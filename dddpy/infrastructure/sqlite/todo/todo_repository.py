"""SQLite implementation of Todo repository."""

from sqlalchemy import desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoId
from dddpy.infrastructure.sqlite.todo import TodoDTO


class TodoRepositoryImpl(TodoRepository):
    """Persist todos using SQLAlchemy and a SQLite backend."""

    def __init__(self, session: Session):
        """Store the SQLAlchemy session dependency.

        Args:
            session: Active SQLAlchemy session bound to the SQLite engine.
        """
        self.session = session

    def find_by_id(self, todo_id: TodoId) -> Todo | None:
        """Return a todo matching the provided identifier.

        Args:
            todo_id: Identifier of the todo to fetch.

        Returns:
            Optional[Todo]: The matching todo when found; otherwise None.
        """
        try:
            row = self.session.query(TodoDTO).filter_by(id=todo_id.value).one()
        except NoResultFound:
            return None

        return row.to_entity()

    def find_all(self) -> list[Todo]:
        """Return todos ordered by creation date with an upper limit.

        Returns:
            List[Todo]: Up to 20 todos sorted by newest first.
        """
        rows = (
            self.session.query(TodoDTO)
            .order_by(desc(TodoDTO.created_at))
            .limit(20)
            .all()
        )
        return [todo_dto.to_entity() for todo_dto in rows]

    def save(self, todo: Todo) -> None:
        """Persist new or updated todo data.

        Args:
            todo: Todo entity to create or update.
        """
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
        """Remove a todo by its identifier.

        Args:
            todo_id: Identifier of the todo to delete.
        """
        self.session.query(TodoDTO).filter_by(id=todo_id.value).delete()


def new_todo_repository(session: Session) -> TodoRepository:
    """Instantiate a SQLite-backed todo repository.

    Args:
        session: Active SQLAlchemy session bound to the SQLite engine.

    Returns:
        TodoRepository: Configured repository implementation.
    """
    return TodoRepositoryImpl(session)
