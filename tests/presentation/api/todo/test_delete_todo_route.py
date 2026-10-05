"""Test cases for the DELETE /todos/{todo_id} route."""

from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from dddpy.domain.todo.exceptions import TodoNotFoundError
from dddpy.domain.todo.value_objects import TodoId
from dddpy.infrastructure.di.injection import get_delete_todo_usecase
from dddpy.presentation.api.todo.handlers.todo_api_route_handler import (
    TodoApiRouteHandler,
)
from dddpy.usecase.todo import DeleteTodoUseCase


@pytest.fixture
def delete_todo_usecase_mock():
    """Create a mock DeleteTodoUseCase."""
    return Mock(spec=DeleteTodoUseCase)


@pytest.fixture
def client(delete_todo_usecase_mock):
    """Create a test client with the delete use case overridden."""
    app = FastAPI()
    TodoApiRouteHandler().register_routes(app)
    app.dependency_overrides[get_delete_todo_usecase] = lambda: delete_todo_usecase_mock
    return TestClient(app)


def test_delete_todo(client, delete_todo_usecase_mock):
    """Test deleting an existing todo returns 204."""
    todo_id = uuid4()

    response = client.delete(f'/todos/{todo_id}')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b''
    delete_todo_usecase_mock.execute.assert_called_once_with(TodoId(todo_id))


def test_delete_todo_not_found(client, delete_todo_usecase_mock):
    """Test deleting a missing todo returns 404."""
    delete_todo_usecase_mock.execute.side_effect = TodoNotFoundError

    response = client.delete(f'/todos/{uuid4()}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': TodoNotFoundError.message}


def test_delete_todo_invalid_id(client, delete_todo_usecase_mock):
    """Test deleting with a malformed identifier returns 422."""
    response = client.delete('/todos/not-a-uuid')

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    delete_todo_usecase_mock.execute.assert_not_called()
