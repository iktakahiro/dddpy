"""Data Transfer Object for ToDo entity in SQLite database."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from dddpy.domain.todo import ToDo, ToDoDescription, ToDoId, ToDoStatus, ToDoTitle
from dddpy.infrastructure.sqlite.database import Base


class ToDoDTO(Base):
    """Data Transfer Object for ToDo entity in SQLite database."""

    __tablename__ = 'todo'
    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(index=True, nullable=False)
    created_at: Mapped[int] = mapped_column(index=True, nullable=False)
    updated_at: Mapped[int] = mapped_column(index=True, nullable=False)
    completed_at: Mapped[int] = mapped_column(index=True, nullable=True)

    def to_entity(self) -> ToDo:
        """Convert DTO to domain entity."""
        return ToDo(
            ToDoId(UUID(self.id)),
            ToDoTitle(self.title),
            ToDoDescription(self.description),
            ToDoStatus(self.status),
            datetime.fromtimestamp(self.created_at),
            datetime.fromtimestamp(self.updated_at),
            datetime.fromtimestamp(self.completed_at) if self.completed_at else None,
        )

    @staticmethod
    def from_entity(todo: ToDo) -> 'ToDoDTO':
        """Convert domain entity to DTO."""
        return ToDoDTO(
            id=todo.id.value,
            title=todo.title.value,
            description=todo.description.value if todo.description else None,
            status=todo.status.value,
            created_at=int(todo.created_at.timestamp()),
            updated_at=int(todo.updated_at.timestamp()),
            completed_at=int(todo.completed_at.timestamp())
            if todo.completed_at
            else None,
        )
