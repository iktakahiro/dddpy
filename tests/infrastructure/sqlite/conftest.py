"""Shared fixtures for SQLite infrastructure tests."""

from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from dddpy.infrastructure.sqlite.database import Base
from dddpy.infrastructure.sqlite.todo import TodoDTO  # noqa: F401  # registers the model


@pytest.fixture
def session() -> Iterator[Session]:
    """Yield a session bound to an isolated in-memory SQLite database.

    Yields:
        Session: Session with all tables created; closed and disposed afterwards.
    """
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db_session:
        yield db_session
    engine.dispose()
