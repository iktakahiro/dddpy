"""Test cases for the GET /todos route."""

from unittest.mock import Mock

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.value_objects import TodoTitle
from dddpy.infrastructure.di.injection import get_find_todos_usecase
from dddpy.presentation.api.todo.handlers.todo_api_route_handler import (
    TodoApiRouteHandler,
)
from dddpy.usecase.todo import FindTodosUseCase


@pytest.fixture
def find_todos_usecase_mock():
    """Create a mock FindTodosUseCase."""
    return Mock(spec=FindTodosUseCase)


@pytest.fixture
def client(find_todos_usecase_mock):
    """Create a test client with the find todos use case overridden."""
    app = FastAPI()
    TodoApiRouteHandler().register_routes(app)
    app.dependency_overrides[get_find_todos_usecase] = lambda: find_todos_usecase_mock
    return TestClient(app)


def test_get_todos(client, find_todos_usecase_mock):
    """Test listing todos returns 200 with the serialized todos."""
    todos = [Todo.create(TodoTitle('first')), Todo.create(TodoTitle('second'))]
    find_todos_usecase_mock.execute.return_value = todos

    response = client.get('/todos')

    assert response.status_code == status.HTTP_200_OK
    assert [item['id'] for item in response.json()] == [
        str(todo.id.value) for todo in todos
    ]
    assert [item['title'] for item in response.json()] == ['first', 'second']
    find_todos_usecase_mock.execute.assert_called_once_with()


def test_get_todos_empty(client, find_todos_usecase_mock):
    """Test listing todos returns an empty list when none exist."""
    find_todos_usecase_mock.execute.return_value = []

    response = client.get('/todos')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_todos_unexpected_error(client, find_todos_usecase_mock):
    """Test an unexpected use case error returns 500."""
    find_todos_usecase_mock.execute.side_effect = RuntimeError('boom')

    response = client.get('/todos')

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {'detail': 'Internal Server Error'}
