"""Error message model for when a Todo item is not started."""

from pydantic import BaseModel, Field

from dddpy.domain.todo.exceptions import TodoNotStartedError


class ErrorMessageTodoNotStarted(BaseModel):
    """Error message model for when a Todo item is not started."""

    detail: str = Field(examples=[TodoNotStartedError.message])
