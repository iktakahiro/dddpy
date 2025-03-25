"""Create model for Todo entities in the application."""

from pydantic import BaseModel, Field


class TodoCreateSchema(BaseModel):
    """TodoCreateSchema represents data structure as a create model."""

    title: str = Field(min_length=1, max_length=100, examples=['Complete the project'])
    description: str | None = Field(
        default=None,
        max_length=1000,
        examples=['Finish implementing the DDD architecture'],
    )
