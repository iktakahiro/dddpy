"""Test cases for the GET /todos/{todo_id} route."""

from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.exceptions import TodoNotFoundError
from dddpy.domain.todo.value_objects import TodoId, TodoTitle
from dddpy.infrastructure.di.injection import get_find_todo_by_id_usecase
from dddpy.presentation.api.todo.handlers.todo_api_route_handler import (
    TodoApiRouteHandler,
)
from dddpy.usecase.todo import FindTodoByIdUseCase


@pytest.fixture
def find_todo_by_id_usecase_mock():
    """Create a mock FindTodoByIdUseCase."""
    return Mock(spec=FindTodoByIdUseCase)


@pytest.fixture
def client(find_todo_by_id_usecase_mock):
    """Create a test client with the find todo by id use case overridden."""
    app = FastAPI()
    TodoApiRouteHandler().register_routes(app)
    app.dependency_overrides[get_find_todo_by_id_usecase] = lambda: (
        find_todo_by_id_usecase_mock
    )
    return TestClient(app)


def test_get_todo(client, find_todo_by_id_usecase_mock):
    """Test fetching an existing todo returns 200."""
    todo = Todo.create(TodoTitle('title'))
    find_todo_by_id_usecase_mock.execute.return_value = todo

    response = client.get(f'/todos/{todo.id.value}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(todo.id.value)
    assert response.json()['title'] == 'title'
    find_todo_by_id_usecase_mock.execute.assert_called_once_with(todo.id)


def test_get_todo_not_found(client, find_todo_by_id_usecase_mock):
    """Test fetching a missing todo returns 404."""
    todo_id = uuid4()
    find_todo_by_id_usecase_mock.execute.side_effect = TodoNotFoundError

    response = client.get(f'/todos/{todo_id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': TodoNotFoundError.message}
    find_todo_by_id_usecase_mock.execute.assert_called_once_with(TodoId(todo_id))


def test_get_todo_invalid_id(client, find_todo_by_id_usecase_mock):
    """Test fetching with a malformed identifier returns 422."""
    response = client.get('/todos/not-a-uuid')

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    find_todo_by_id_usecase_mock.execute.assert_not_called()
