"""Database configuration and session management for SQLite."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./db/sqlite.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        'check_same_thread': False,
    },
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=True,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy declarative models."""


def create_tables():
    """Create all database tables defined in SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)
