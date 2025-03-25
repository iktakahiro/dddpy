"""Query model for Todo entities in the application."""

from pydantic import BaseModel, Field

from dddpy.domain.todo.entities import Todo


class TodoSchema(BaseModel):
    """TodoQueryModel represents data structure as a read model."""

    id: str = Field(examples=['123e4567-e89b-12d3-a456-426614174000'])
    title: str = Field(examples=['Complete the project'])
    description: str = Field(examples=['Finish implementing the DDD architecture'])
    status: str = Field(examples=['not_started'])
    created_at: int = Field(examples=[1136214245000])
    updated_at: int = Field(examples=[1136214245000])
    completed_at: int | None = Field(examples=[1136214245000])

    class Config:
        """Configuration for Pydantic model."""

        from_attributes = True

    @staticmethod
    def from_entity(todo: Todo) -> 'TodoSchema':
        """Convert a Todo entity to a TodoQueryModel."""
        return TodoSchema(
            id=str(todo.id.value),
            title=todo.title.value if todo.title else '',
            description=todo.description.value if todo.description else '',
            status=todo.status.value,
            created_at=int(todo.created_at.timestamp() * 1000),
            updated_at=int(todo.updated_at.timestamp() * 1000),
            completed_at=int(todo.completed_at.timestamp() * 1000)
            if todo.completed_at
            else None,
        )
