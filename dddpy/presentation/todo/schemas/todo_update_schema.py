"""Update model for Todo entities in the application."""

from pydantic import BaseModel, Field


class TodoUpdateSchema(BaseModel):
    """TodoUpdateScheme represents data structure as an update model."""

    title: str = Field(min_length=1, max_length=100, examples=['Complete the project'])
    description: str | None = Field(
        default=None,
        max_length=1000,
        examples=['Finish implementing the DDD architecture'],
    )
