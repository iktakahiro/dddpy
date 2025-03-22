"""Main application entry point for the API."""

import logging
from contextlib import asynccontextmanager
from logging import config

from fastapi import FastAPI

from dddpy.controllers.todo.todo_controller import TodoController
from dddpy.infrastructure.sqlite.database import Base, create_tables, engine

config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables on startup and cleanup on shutdown."""
    create_tables()
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)

todo_controller = TodoController()
todo_controller.register_routes(app)
