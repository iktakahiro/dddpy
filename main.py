"""Main application entry point for the API."""

import logging
from contextlib import asynccontextmanager
from logging import config

from fastapi import FastAPI

from dddpy.controllers.todo.todo_controller import TodoController
from dddpy.infrastructure.sqlite.database import create_tables, engine

config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables on startup and cleanup on shutdown."""
    create_tables()
    yield
    engine.dispose()


app = FastAPI(
    title='DDD Todo API',
    description='A RESTful API for managing todos using Domain-Driven Design principles.',
    version='2.0.0',
    lifespan=lifespan,
)

todo_controller = TodoController()
todo_controller.register_routes(app)
