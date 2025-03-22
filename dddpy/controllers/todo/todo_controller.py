"""Controller for handling Todo-related HTTP requests."""

from typing import List
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status

from dddpy.controllers.todo.todo_error_message import ErrorMessageTodoNotFound
from dddpy.controllers.todo.todo_scheme import (
    TodoCreateScheme,
    TodoScheme,
    TodoUpdateScheme,
)
from dddpy.domain.todo import (
    TodoAlreadyCompletedError,
    TodoAlreadyStartedError,
    TodoDescription,
    TodoId,
    TodoNotFoundError,
    TodoTitle,
)
from dddpy.infrastructure.di import get_todo_command_usecase, get_todo_query_usecase
from dddpy.usecase.todo import TodoCommandUseCase, TodoQueryUseCase


class TodoController:
    """Controller class for handling Todo-related HTTP endpoints."""

    def register_routes(self, app: FastAPI):
        """Register Todo-related routes to the FastAPI application."""

        @app.get(
            '/todos',
            response_model=List[TodoScheme],
            status_code=200,
        )
        def get_todos(usecase: TodoQueryUseCase = Depends(get_todo_query_usecase)):
            try:
                data = usecase.fetch_todos()
                return [TodoScheme.from_entity(todo) for todo in data]
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ) from e

        @app.get(
            '/todos/{todo_id}',
            response_model=TodoScheme,
            status_code=200,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'model': ErrorMessageTodoNotFound,
                },
            },
        )
        def get_todo(
            todo_id: str, usecase: TodoQueryUseCase = Depends(get_todo_query_usecase)
        ):
            uuid = TodoId(UUID(todo_id))
            try:
                todo = usecase.fetch_todo_by_id(uuid)
            except TodoNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.message,
                ) from e
            except Exception as exc:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ) from exc
            return todo

        @app.post(
            '/todos',
            response_model=TodoScheme,
            status_code=201,
            responses={
                status.HTTP_400_BAD_REQUEST: {},
            },
        )
        def create_todo(
            data: TodoCreateScheme,
            usecase: TodoCommandUseCase = Depends(get_todo_command_usecase),
        ):
            try:
                title = TodoTitle(data.title)
                description = (
                    TodoDescription(data.description) if data.description else None
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e,
                ) from e

            try:
                todo = usecase.create_todo(title, description)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ) from e

            return TodoScheme.from_entity(todo)

        @app.put(
            '/todos/{todo_id}',
            status_code=204,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'model': ErrorMessageTodoNotFound,
                },
            },
        )
        def update_todo(
            todo_id: str,
            data: TodoUpdateScheme,
            usecase: TodoCommandUseCase = Depends(get_todo_command_usecase),
        ):
            uuid = TodoId(UUID(todo_id))

            try:
                title = TodoTitle(data.title)
                description = (
                    TodoDescription(data.description) if data.description else None
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e,
                ) from e

            try:
                usecase.update_todo(uuid, title, description)
            except TodoNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.message,
                ) from e
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ) from e

            return None

        @app.patch(
            '/todos/{todo_id}/start',
            status_code=204,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'model': ErrorMessageTodoNotFound,
                },
            },
        )
        def start_todo(
            todo_id: str,
            usecase: TodoCommandUseCase = Depends(get_todo_command_usecase),
        ):
            uuid = TodoId(UUID(todo_id))
            try:
                usecase.start_todo(uuid)
            except TodoNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.message,
                ) from e
            except TodoAlreadyStartedError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e.message,
                ) from e
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ) from e

            return None

        @app.patch(
            '/todos/{todo_id}/complete',
            status_code=204,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'model': ErrorMessageTodoNotFound,
                },
            },
        )
        def complete_todo(
            todo_id: str,
            usecase: TodoCommandUseCase = Depends(get_todo_command_usecase),
        ):
            uuid = TodoId(UUID(todo_id))
            try:
                usecase.complete_todo(uuid)
            except TodoNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.message,
                ) from e
            except TodoAlreadyCompletedError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e.message,
                ) from e
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ) from e

            return None
