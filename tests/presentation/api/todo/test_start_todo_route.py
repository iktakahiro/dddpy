"""Test cases for the PATCH /todos/{todo_id}/start route."""

from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.exceptions import (
    TodoAlreadyCompletedError,
    TodoAlreadyStartedError,
    TodoNotFoundError,
)
from dddpy.domain.todo.value_objects import TodoId, TodoStatus, TodoTitle
from dddpy.infrastructure.di.injection import get_start_todo_usecase
from dddpy.presentation.api.todo.handlers.todo_api_route_handler import (
    TodoApiRouteHandler,
)
from dddpy.usecase.todo import StartTodoUseCase


@pytest.fixture
def start_todo_usecase_mock():
    """Create a mock StartTodoUseCase."""
    return Mock(spec=StartTodoUseCase)


@pytest.fixture
def client(start_todo_usecase_mock):
    """Create a test client with the start use case overridden."""
    app = FastAPI()
    TodoApiRouteHandler().register_routes(app)
    app.dependency_overrides[get_start_todo_usecase] = lambda: start_todo_usecase_mock
    return TestClient(app)


def test_start_todo(client, start_todo_usecase_mock):
    """Test starting a todo returns 200 with the in-progress todo."""
    todo_id = uuid4()
    todo = Todo(TodoId(todo_id), TodoTitle('title'), status=TodoStatus.IN_PROGRESS)
    start_todo_usecase_mock.execute.return_value = todo

    response = client.patch(f'/todos/{todo_id}/start')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(todo_id)
    assert response.json()['status'] == TodoStatus.IN_PROGRESS.value
    start_todo_usecase_mock.execute.assert_called_once_with(TodoId(todo_id))


def test_start_todo_not_found(client, start_todo_usecase_mock):
    """Test starting a missing todo returns 404."""
    todo_id = uuid4()
    start_todo_usecase_mock.execute.side_effect = TodoNotFoundError

    response = client.patch(f'/todos/{todo_id}/start')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': TodoNotFoundError.message}
    start_todo_usecase_mock.execute.assert_called_once_with(TodoId(todo_id))


def test_start_todo_already_started(client, start_todo_usecase_mock):
    """Test starting an in-progress todo returns 400."""
    todo_id = uuid4()
    start_todo_usecase_mock.execute.side_effect = TodoAlreadyStartedError

    response = client.patch(f'/todos/{todo_id}/start')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': TodoAlreadyStartedError.message}
    start_todo_usecase_mock.execute.assert_called_once_with(TodoId(todo_id))


def test_start_todo_already_completed(client, start_todo_usecase_mock):
    """Test starting a completed todo returns 400."""
    todo_id = uuid4()
    start_todo_usecase_mock.execute.side_effect = TodoAlreadyCompletedError

    response = client.patch(f'/todos/{todo_id}/start')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': TodoAlreadyCompletedError.message}
    start_todo_usecase_mock.execute.assert_called_once_with(TodoId(todo_id))
