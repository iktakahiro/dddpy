"""Error message models for Todo-related API responses."""

from pydantic import BaseModel, Field

from dddpy.domain.todo.todo_exception import (
    TodoAlreadyCompletedError,
    TodoAlreadyStartedError,
    TodoNotFoundError,
    TodoNotStartedError,
)


class ErrorMessageTodoNotFound(BaseModel):
    """Error message model for when a Todo item is not found."""

    detail: str = Field(examples=[TodoNotFoundError.message])


class ErrorMessageTodoAlreadyCompleted(BaseModel):
    """Error message model for when a Todo item is already completed."""

    detail: str = Field(examples=[TodoAlreadyCompletedError.message])


class ErrorMessageTodoAlreadyStarted(BaseModel):
    """Error message model for when a Todo item is already started."""

    detail: str = Field(examples=[TodoAlreadyStartedError.message])


class ErrorMessageTodoNotStarted(BaseModel):
    """Error message model for when a Todo item is not started."""

    detail: str = Field(examples=[TodoNotStartedError.message])
