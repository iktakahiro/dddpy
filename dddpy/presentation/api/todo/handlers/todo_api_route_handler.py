"""Controller for handling Todo-related HTTP requests."""

from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status

from dddpy.domain.todo.exceptions import (
    TodoAlreadyCompletedError,
    TodoAlreadyStartedError,
    TodoNotFoundError,
    TodoNotStartedError,
)
from dddpy.domain.todo.value_objects import TodoDescription, TodoId, TodoTitle
from dddpy.infrastructure.di.injection import (
    get_complete_todo_usecase,
    get_create_todo_usecase,
    get_find_todo_by_id_usecase,
    get_find_todos_usecase,
    get_start_todo_usecase,
    get_update_todo_usecase,
)
from dddpy.presentation.api.todo.error_messages import ErrorMessageTodoNotFound
from dddpy.presentation.api.todo.schemas import (
    TodoCreateSchema,
    TodoSchema,
    TodoUpdateSchema,
)
from dddpy.usecase.todo import (
    CompleteTodoUseCase,
    CreateTodoUseCase,
    FindTodoByIdUseCase,
    FindTodosUseCase,
    StartTodoUseCase,
    UpdateTodoUseCase,
)


class TodoApiRouteHandler:
    """Register HTTP endpoints that expose todo use cases."""

    def register_routes(self, app: FastAPI) -> None:
        """Attach todo routes to the provided FastAPI application.

        Args:
            app: FastAPI instance that receives the todo routes.
        """
        self._register_get_todos_route(app)
        self._register_get_todo_route(app)
        self._register_create_todo_route(app)
        self._register_update_todo_route(app)
        self._register_start_todo_route(app)
        self._register_complete_todo_route(app)

    @staticmethod
    def _build_todo_description(description: str | None) -> TodoDescription | None:
        """Convert an optional description string into a value object."""
        return TodoDescription(description) if description else None

    def _register_get_todos_route(self, app: FastAPI) -> None:
        """Register the route that returns all todos."""

        @app.get(
            '/todos',
            response_model=list[TodoSchema],
            status_code=200,
        )
        def get_todos(
            usecase: FindTodosUseCase = Depends(get_find_todos_usecase),
        ) -> list[TodoSchema]:
            """Return the latest todos.

            Args:
                usecase: Use case responsible for retrieving todos.

            Returns:
                list[TodoSchema]: Serialized todos returned to the client.

            Raises:
                HTTPException: When the use case raises an unexpected error.
            """
            try:
                data = usecase.execute()
                return [TodoSchema.from_entity(todo) for todo in data]
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ) from e

    def _register_get_todo_route(self, app: FastAPI) -> None:
        """Register the route that returns a single todo."""

        @app.get(
            '/todos/{todo_id}',
            response_model=TodoSchema,
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
        ) -> TodoSchema:
            """Return a single todo by identifier.

            Args:
                todo_id: Identifier of the requested todo.
                usecase: Use case responsible for todo retrieval.

            Returns:
                TodoSchema: Serialized todo returned to the client.

            Raises:
                HTTPException: When the todo is missing or an unexpected error occurs.
            """
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
            return TodoSchema.from_entity(todo)

    def _register_create_todo_route(self, app: FastAPI) -> None:
        """Register the route that creates a todo."""

        @app.post(
            '/todos',
            response_model=TodoSchema,
            status_code=201,
            responses={
                status.HTTP_400_BAD_REQUEST: {},
            },
        )
        def create_todo(
            data: TodoCreateSchema,
            usecase: CreateTodoUseCase = Depends(get_create_todo_usecase),
        ) -> TodoSchema:
            """Create a todo from the request payload.

            Args:
                data: Payload containing todo creation fields.
                usecase: Use case responsible for creating todos.

            Returns:
                TodoSchema: Serialized todo returned to the client.

            Raises:
                HTTPException: When validation or use case execution fails.
            """
            try:
                title = TodoTitle(data.title)
                description = self._build_todo_description(data.description)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e),
                ) from e

            try:
                todo = usecase.execute(title, description)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ) from e

            return TodoSchema.from_entity(todo)

    def _register_update_todo_route(self, app: FastAPI) -> None:
        """Register the route that updates an existing todo."""

        @app.put(
            '/todos/{todo_id}',
            response_model=TodoSchema,
            status_code=200,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'model': ErrorMessageTodoNotFound,
                },
            },
        )
        def update_todo(
            todo_id: UUID,
            data: TodoUpdateSchema,
            usecase: UpdateTodoUseCase = Depends(get_update_todo_usecase),
        ) -> TodoSchema:
            """Update a todo identified by the path parameter.

            Args:
                todo_id: Identifier of the todo to update.
                data: Payload containing fields to update.
                usecase: Use case responsible for updating todos.

            Returns:
                TodoSchema: Serialized todo returned to the client.

            Raises:
                HTTPException: When validation fails or the todo cannot be updated.
            """
            _id = TodoId(todo_id)

            try:
                title = TodoTitle(data.title)
                description = self._build_todo_description(data.description)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e),
                ) from e

            try:
                todo = usecase.execute(_id, title, description)
            except TodoNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.message,
                ) from e
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                ) from e

            return TodoSchema.from_entity(todo)

    def _register_start_todo_route(self, app: FastAPI) -> None:
        """Register the route that starts a todo."""

        @app.patch(
            '/todos/{todo_id}/start',
            response_model=TodoSchema,
            status_code=200,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'model': ErrorMessageTodoNotFound,
                },
            },
        )
        def start_todo(
            todo_id: UUID,
            usecase: StartTodoUseCase = Depends(get_start_todo_usecase),
        ) -> TodoSchema:
            """Start a todo via the corresponding use case.

            Args:
                todo_id: Identifier of the todo to start.
                usecase: Use case responsible for starting todos.

            Returns:
                TodoSchema: Serialized todo returned to the client.

            Raises:
                HTTPException: When lifecycle rules prevent the transition.
            """
            _id = TodoId(todo_id)
            try:
                todo = usecase.execute(_id)
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

            return TodoSchema.from_entity(todo)

    def _register_complete_todo_route(self, app: FastAPI) -> None:
        """Register the route that completes a todo."""

        @app.patch(
            '/todos/{todo_id}/complete',
            response_model=TodoSchema,
            status_code=200,
            responses={
                status.HTTP_404_NOT_FOUND: {
                    'model': ErrorMessageTodoNotFound,
                },
            },
        )
        def complete_todo(
            todo_id: UUID,
            usecase: CompleteTodoUseCase = Depends(get_complete_todo_usecase),
        ) -> TodoSchema:
            """Complete a todo via the corresponding use case.

            Args:
                todo_id: Identifier of the todo to complete.
                usecase: Use case responsible for completing todos.

            Returns:
                TodoSchema: Serialized todo returned to the client.

            Raises:
                HTTPException: When lifecycle rules prevent completion.
            """
            _id = TodoId(todo_id)
            try:
                todo = usecase.execute(_id)
            except TodoNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.message,
                ) from e
            except TodoNotStartedError as e:
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

            return TodoSchema.from_entity(todo)
