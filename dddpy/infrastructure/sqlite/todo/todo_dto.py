"""Map todo entities to and from SQLite persistence models."""

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.value_objects import (
    TodoDescription,
    TodoId,
    TodoStatus,
    TodoTitle,
)
from dddpy.infrastructure.sqlite.database import Base


class TodoDTO(Base):
    """Represent the SQLite persistence model for todos."""

    __tablename__ = 'todo'
    id: Mapped[UUID] = mapped_column(primary_key=True, autoincrement=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(index=True, nullable=False)
    created_at: Mapped[int] = mapped_column(index=True, nullable=False)
    updated_at: Mapped[int] = mapped_column(index=True, nullable=False)
    completed_at: Mapped[int | None] = mapped_column(index=True, nullable=True)

    def to_entity(self) -> Todo:
        """Convert the DTO into a domain entity.

        Returns:
            Todo: Domain entity reconstructed from persisted values.
        """
        return Todo(
            TodoId(self.id),
            TodoTitle(self.title),
            TodoDescription(self.description) if self.description else None,
            TodoStatus(self.status),
            datetime.fromtimestamp(self.created_at / 1000, tz=UTC),
            datetime.fromtimestamp(self.updated_at / 1000, tz=UTC),
            datetime.fromtimestamp(self.completed_at / 1000, tz=UTC)
            if self.completed_at
            else None,
        )

    @staticmethod
    def from_entity(todo: Todo) -> 'TodoDTO':
        """Create a DTO from a domain entity.

        Args:
            todo: Domain entity to convert.

        Returns:
            TodoDTO: DTO populated for persistence.
        """
        return TodoDTO(
            id=todo.id.value,
            title=todo.title.value,
            description=todo.description.value if todo.description else None,
            status=todo.status.value,
            created_at=int(todo.created_at.timestamp() * 1000),
            updated_at=int(todo.updated_at.timestamp() * 1000),
            completed_at=int(todo.completed_at.timestamp() * 1000)
            if todo.completed_at
            else None,
        )
