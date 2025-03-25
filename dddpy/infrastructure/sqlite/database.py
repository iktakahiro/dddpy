"""Database configuration and session management for SQLite."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


Base = declarative_base()


def create_tables():
    """Create all database tables defined in SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)
