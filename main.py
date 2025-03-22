"""Main application entry point for the API."""

import logging
from logging import config

from fastapi import FastAPI

from dddpy.controllers.todo.todo_controller import TodoController
from dddpy.infrastructure.sqlite.database import create_tables

config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

todo_controller = TodoController()
todo_controller.register_routes(app)


create_tables()
