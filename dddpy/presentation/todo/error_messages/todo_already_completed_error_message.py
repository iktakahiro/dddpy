"""Error message model for when a Todo item is already completed."""

from pydantic import BaseModel, Field

from dddpy.domain.todo.exceptions import TodoAlreadyCompletedError


class ErrorMessageTodoAlreadyCompleted(BaseModel):
    """Error message model for when a Todo item is already completed."""

    detail: str = Field(examples=[TodoAlreadyCompletedError.message])
