"""Query model for Todo entities in the application."""

from pydantic import BaseModel, Field

from dddpy.domain.todo.entities import Todo


class TodoScheme(BaseModel):
    """TodoQueryModel represents data structure as a read model."""

    id: str = Field(examples=['vytxeTZskVKR7C7WgdSP3d'])
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
    def from_entity(todo: Todo) -> 'TodoScheme':
        """Convert a Todo entity to a TodoQueryModel."""
        return TodoScheme(
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


class TodoCreateScheme(BaseModel):
    """TodoCreateScheme represents data structure as a create model."""

    title: str = Field(min_length=1, max_length=100, examples=['Complete the project'])
    description: str | None = Field(
        default=None,
        max_length=1000,
        examples=['Finish implementing the DDD architecture'],
    )


class TodoUpdateScheme(BaseModel):
    """TodoUpdateScheme represents data structure as an update model."""

    title: str = Field(min_length=1, max_length=100, examples=['Complete the project'])
    description: str | None = Field(
        default=None,
        max_length=1000,
        examples=['Finish implementing the DDD architecture'],
    )
