"""Test cases for the PATCH /todos/{todo_id}/complete route."""

from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.exceptions import (
    TodoAlreadyCompletedError,
    TodoNotFoundError,
    TodoNotStartedError,
)
from dddpy.domain.todo.value_objects import TodoId, TodoStatus, TodoTitle
from dddpy.infrastructure.di.injection import get_complete_todo_usecase
from dddpy.presentation.api.todo.handlers.todo_api_route_handler import (
    TodoApiRouteHandler,
)
from dddpy.usecase.todo import CompleteTodoUseCase


@pytest.fixture
def complete_todo_usecase_mock():
    """Create a mock CompleteTodoUseCase."""
    return Mock(spec=CompleteTodoUseCase)


@pytest.fixture
def client(complete_todo_usecase_mock):
    """Create a test client with the complete use case overridden."""
    app = FastAPI()
    TodoApiRouteHandler().register_routes(app)
    app.dependency_overrides[get_complete_todo_usecase] = lambda: (
        complete_todo_usecase_mock
    )
    return TestClient(app)


def test_complete_todo(client, complete_todo_usecase_mock):
    """Test completing a todo returns 200 with the completed todo."""
    todo_id = uuid4()
    todo = Todo(TodoId(todo_id), TodoTitle('title'), status=TodoStatus.COMPLETED)
    complete_todo_usecase_mock.execute.return_value = todo

    response = client.patch(f'/todos/{todo_id}/complete')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(todo_id)
    assert response.json()['status'] == TodoStatus.COMPLETED.value
    complete_todo_usecase_mock.execute.assert_called_once_with(TodoId(todo_id))


def test_complete_todo_not_found(client, complete_todo_usecase_mock):
    """Test completing a missing todo returns 404."""
    todo_id = uuid4()
    complete_todo_usecase_mock.execute.side_effect = TodoNotFoundError

    response = client.patch(f'/todos/{todo_id}/complete')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': TodoNotFoundError.message}
    complete_todo_usecase_mock.execute.assert_called_once_with(TodoId(todo_id))


def test_complete_todo_not_started(client, complete_todo_usecase_mock):
    """Test completing a todo that was never started returns 400."""
    todo_id = uuid4()
    complete_todo_usecase_mock.execute.side_effect = TodoNotStartedError

    response = client.patch(f'/todos/{todo_id}/complete')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': TodoNotStartedError.message}
    complete_todo_usecase_mock.execute.assert_called_once_with(TodoId(todo_id))


def test_complete_todo_already_completed(client, complete_todo_usecase_mock):
    """Test completing a completed todo returns 400."""
    todo_id = uuid4()
    complete_todo_usecase_mock.execute.side_effect = TodoAlreadyCompletedError

    response = client.patch(f'/todos/{todo_id}/complete')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': TodoAlreadyCompletedError.message}
    complete_todo_usecase_mock.execute.assert_called_once_with(TodoId(todo_id))
