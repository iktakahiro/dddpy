"""Error message model for when a Todo item is not found."""

from pydantic import BaseModel, Field

from dddpy.domain.todo.exceptions import TodoNotFoundError


class ErrorMessageTodoNotFound(BaseModel):
    """Error message model for when a Todo item is not found."""

    detail: str = Field(examples=[TodoNotFoundError.message])
