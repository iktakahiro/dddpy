"""Dependency injection configuration for the application."""

from typing import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from dddpy.infrastructure.sqlite.database import SessionLocal
from dddpy.infrastructure.sqlite.todo.todo_repository import TodoRepositoryImpl
from dddpy.usecase.todo.todo_command_usecase import (
    TodoCommandUseCase,
    TodoCommandUseCaseImpl,
)
from dddpy.usecase.todo.todo_query_usecase import TodoQueryUseCase, TodoQueryUseCaseImpl


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


def get_todo_query_usecase(
    session: Session = Depends(get_session),
) -> TodoQueryUseCase:
    """Get a TodoQueryUseCase instance with dependencies injected."""
    todo_repository = TodoRepositoryImpl(session)
    return TodoQueryUseCaseImpl(todo_repository)


def get_todo_command_usecase(
    session: Session = Depends(get_session),
) -> TodoCommandUseCase:
    """Get a TodoCommandUseCase instance with dependencies injected."""
    todo_repository = TodoRepositoryImpl(session)
    return TodoCommandUseCaseImpl(todo_repository)
