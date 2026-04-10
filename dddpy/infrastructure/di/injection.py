"""Dependency injection configuration for the application."""

from collections.abc import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from dddpy.domain.todo.repositories import TodoRepository
from dddpy.infrastructure.sqlite.database import SessionLocal
from dddpy.infrastructure.sqlite.todo.todo_repository import new_todo_repository
from dddpy.usecase.todo import (
    CompleteTodoUseCase,
    CreateTodoUseCase,
    DeleteTodoUseCase,
    FindTodoByIdUseCase,
    FindTodosUseCase,
    StartTodoUseCase,
    UpdateTodoUseCase,
    new_complete_todo_usecase,
    new_create_todo_usecase,
    new_delete_todo_usecase,
    new_find_todo_by_id_usecase,
    new_find_todos_usecase,
    new_start_todo_usecase,
    new_update_todo_usecase,
)


def get_session() -> Iterator[Session]:
    """Yield a managed SQLAlchemy session for request handling.

    Yields:
        Session: Database session with automatic commit or rollback.

    Raises:
        Exception: Propagates any database or application error after rollback.
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_todo_repository(session: Session = Depends(get_session)) -> TodoRepository:
    """Provide a repository instance bound to the current session.

    Args:
        session: Active SQLAlchemy session provided by FastAPI.

    Returns:
        TodoRepository: Repository configured with the session.
    """
    return new_todo_repository(session)


def get_create_todo_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> CreateTodoUseCase:
    """Provide the create-todo use case with injected repository.

    Args:
        todo_repository: Repository dependency supplied by FastAPI.

    Returns:
        CreateTodoUseCase: Configured use case implementation.
    """
    return new_create_todo_usecase(todo_repository)


def get_start_todo_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> StartTodoUseCase:
    """Provide the start-todo use case with injected repository.

    Args:
        todo_repository: Repository dependency supplied by FastAPI.

    Returns:
        StartTodoUseCase: Configured use case implementation.
    """
    return new_start_todo_usecase(todo_repository)


def get_complete_todo_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> CompleteTodoUseCase:
    """Provide the complete-todo use case with injected repository.

    Args:
        todo_repository: Repository dependency supplied by FastAPI.

    Returns:
        CompleteTodoUseCase: Configured use case implementation.
    """
    return new_complete_todo_usecase(todo_repository)


def get_update_todo_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> UpdateTodoUseCase:
    """Provide the update-todo use case with injected repository.

    Args:
        todo_repository: Repository dependency supplied by FastAPI.

    Returns:
        UpdateTodoUseCase: Configured use case implementation.
    """
    return new_update_todo_usecase(todo_repository)


def get_delete_todo_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> DeleteTodoUseCase:
    """Provide the delete-todo use case with injected repository.

    Args:
        todo_repository: Repository dependency supplied by FastAPI.

    Returns:
        DeleteTodoUseCase: Configured use case implementation.
    """
    return new_delete_todo_usecase(todo_repository)


def get_find_todo_by_id_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> FindTodoByIdUseCase:
    """Provide the find-by-id use case with injected repository.

    Args:
        todo_repository: Repository dependency supplied by FastAPI.

    Returns:
        FindTodoByIdUseCase: Configured use case implementation.
    """
    return new_find_todo_by_id_usecase(todo_repository)


def get_find_todos_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> FindTodosUseCase:
    """Provide the list-todos use case with injected repository.

    Args:
        todo_repository: Repository dependency supplied by FastAPI.

    Returns:
        FindTodosUseCase: Configured use case implementation.
    """
    return new_find_todos_usecase(todo_repository)
