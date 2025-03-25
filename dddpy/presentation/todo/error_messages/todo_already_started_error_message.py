"""Error message model for when a Todo item is already started."""

from pydantic import BaseModel, Field

from dddpy.domain.todo.exceptions import TodoAlreadyStartedError


class ErrorMessageTodoAlreadyStarted(BaseModel):
    """Error message model for when a Todo item is already started."""

    detail: str = Field(examples=[TodoAlreadyStartedError.message])
