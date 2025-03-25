"""Dependency injection configuration for the application."""

from typing import Iterator

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
    """Get a session from the database."""
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
    """Get a TodoRepository instance with dependencies injected."""
    return new_todo_repository(session)


def get_create_todo_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> CreateTodoUseCase:
    """Get a CreateTodoUseCase instance with dependencies injected."""
    return new_create_todo_usecase(todo_repository)


def get_start_todo_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> StartTodoUseCase:
    """Get a StartTodoUseCase instance with dependencies injected."""
    return new_start_todo_usecase(todo_repository)


def get_complete_todo_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> CompleteTodoUseCase:
    """Get a CompleteTodoUseCase instance with dependencies injected."""
    return new_complete_todo_usecase(todo_repository)


def get_update_todo_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> UpdateTodoUseCase:
    """Get an UpdateTodoUseCase instance with dependencies injected."""
    return new_update_todo_usecase(todo_repository)


def get_delete_todo_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> DeleteTodoUseCase:
    """Get a DeleteTodoUseCase instance with dependencies injected."""
    return new_delete_todo_usecase(todo_repository)


def get_find_todo_by_id_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> FindTodoByIdUseCase:
    """Get a FindTodoByIdUseCase instance with dependencies injected."""
    return new_find_todo_by_id_usecase(todo_repository)


def get_find_todos_usecase(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> FindTodosUseCase:
    """Get a FindTodosUseCase instance with dependencies injected."""
    return new_find_todos_usecase(todo_repository)
