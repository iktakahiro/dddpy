"""Expose the error schema returned when todo fields violate a domain rule."""

from pydantic import BaseModel, Field

from dddpy.domain.todo.value_objects.todo_title import TITLE_REQUIRED_ERROR_MESSAGE


class ErrorMessageInvalidTodo(BaseModel):
    """Represent the invalid-todo-fields error response payload."""

    detail: str = Field(examples=[TITLE_REQUIRED_ERROR_MESSAGE])
