"""Test cases for the PUT /todos/{todo_id} route."""

from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.exceptions import TodoNotFoundError
from dddpy.domain.todo.value_objects import TodoDescription, TodoId, TodoTitle
from dddpy.domain.todo.value_objects.todo_title import TITLE_REQUIRED_ERROR_MESSAGE
from dddpy.infrastructure.di.injection import get_update_todo_usecase
from dddpy.presentation.api.todo.handlers import todo_api_route_handler
from dddpy.presentation.api.todo.handlers.todo_api_route_handler import (
    TodoApiRouteHandler,
)
from dddpy.usecase.todo import UpdateTodoUseCase


@pytest.fixture
def update_todo_usecase_mock():
    """Create a mock UpdateTodoUseCase."""
    return Mock(spec=UpdateTodoUseCase)


@pytest.fixture
def client(update_todo_usecase_mock):
    """Create a test client with the update use case overridden."""
    app = FastAPI()
    TodoApiRouteHandler().register_routes(app)
    app.dependency_overrides[get_update_todo_usecase] = lambda: update_todo_usecase_mock
    return TestClient(app)


def test_update_todo(client, update_todo_usecase_mock):
    """Test updating a todo returns 200 and passes value objects."""
    todo_id = uuid4()
    update_todo_usecase_mock.execute.return_value = Todo(
        TodoId(todo_id), TodoTitle('new title'), TodoDescription('new description')
    )

    response = client.put(
        f'/todos/{todo_id}',
        json={'title': 'new title', 'description': 'new description'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(todo_id)
    assert response.json()['title'] == 'new title'
    assert response.json()['description'] == 'new description'
    update_todo_usecase_mock.execute.assert_called_once_with(
        TodoId(todo_id), TodoTitle('new title'), TodoDescription('new description')
    )


def test_update_todo_without_description(client, update_todo_usecase_mock):
    """Test omitting the description passes None to the use case."""
    todo_id = uuid4()
    update_todo_usecase_mock.execute.return_value = Todo(
        TodoId(todo_id), TodoTitle('new title')
    )

    response = client.put(f'/todos/{todo_id}', json={'title': 'new title'})

    assert response.status_code == status.HTTP_200_OK
    update_todo_usecase_mock.execute.assert_called_once_with(
        TodoId(todo_id), TodoTitle('new title'), None
    )


def test_update_todo_invalid_title(client, update_todo_usecase_mock, monkeypatch):
    """Test a domain validation error is mapped to 400.

    The request schema already rejects empty and over-long titles with 422, so
    the value object is made to fail to exercise the 400 mapping directly.
    """

    def raise_value_error(_value: str) -> TodoTitle:
        raise ValueError(TITLE_REQUIRED_ERROR_MESSAGE)

    monkeypatch.setattr(todo_api_route_handler, 'TodoTitle', raise_value_error)

    response = client.put(f'/todos/{uuid4()}', json={'title': 'title'})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': TITLE_REQUIRED_ERROR_MESSAGE}
    update_todo_usecase_mock.execute.assert_not_called()


def test_update_todo_empty_title_rejected_by_schema(client, update_todo_usecase_mock):
    """Test an empty title is rejected by request validation with 422."""
    response = client.put(f'/todos/{uuid4()}', json={'title': ''})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    update_todo_usecase_mock.execute.assert_not_called()


def test_update_todo_not_found(client, update_todo_usecase_mock):
    """Test updating a missing todo returns 404."""
    todo_id = uuid4()
    update_todo_usecase_mock.execute.side_effect = TodoNotFoundError

    response = client.put(f'/todos/{todo_id}', json={'title': 'title'})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': TodoNotFoundError.message}
    update_todo_usecase_mock.execute.assert_called_once_with(
        TodoId(todo_id), TodoTitle('title'), None
    )
