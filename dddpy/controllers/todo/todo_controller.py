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
from dddpy.infrastructure.di.injection import (
    get_complete_todo_usecase,
    get_create_todo_usecase,
    get_find_todo_by_id_usecase,
    get_find_todos_usecase,
    get_start_todo_usecase,
    get_update_todo_usecase,
)
from dddpy.usecase.todo import (
    CompleteTodoUseCase,
    CreateTodoUseCase,
    FindTodoByIdUseCase,
    FindTodosUseCase,
    StartTodoUseCase,
    UpdateTodoUseCase,
)


class TodoController:
    """Controller class for handling Todo-related HTTP endpoints."""

    def register_routes(self, app: FastAPI):
        """Register Todo-related routes to the FastAPI application."""

        @app.get(
            '/todos',
            response_model=List[TodoScheme],
            status_code=200,
        )
        def get_todos(
            usecase: FindTodosUseCase = Depends(get_find_todos_usecase),
        ):
            try:
                data = usecase.execute()
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
            todo_id: UUID,
            usecase: FindTodoByIdUseCase = Depends(get_find_todo_by_id_usecase),
        ):
            uuid = TodoId(todo_id)
            try:
                todo = usecase.execute(uuid)
            except TodoNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.message,
                ) from e
            except Exception as exc:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ) from exc
            return TodoScheme.from_entity(todo)

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
            usecase: CreateTodoUseCase = Depends(get_create_todo_usecase),
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
                todo = usecase.execute(title, description)
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
            todo_id: UUID,
            data: TodoUpdateScheme,
            usecase: UpdateTodoUseCase = Depends(get_update_todo_usecase),
        ):
            _id = TodoId(todo_id)

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
                usecase.execute(_id, title, description)
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
            todo_id: UUID,
            usecase: StartTodoUseCase = Depends(get_start_todo_usecase),
        ):
            _id = TodoId(todo_id)
            try:
                usecase.execute(_id)
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
            todo_id: UUID,
            usecase: CompleteTodoUseCase = Depends(get_complete_todo_usecase),
        ):
            _id = TodoId(todo_id)
            try:
                usecase.execute(_id)
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
