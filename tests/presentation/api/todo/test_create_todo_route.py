"""Test cases for the POST /todos route."""

from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.value_objects import TodoDescription, TodoId, TodoTitle
from dddpy.domain.todo.value_objects.todo_description import (
    DESCRIPTION_TOO_LONG_ERROR_MESSAGE,
)
from dddpy.domain.todo.value_objects.todo_title import TITLE_REQUIRED_ERROR_MESSAGE
from dddpy.infrastructure.di.injection import get_create_todo_usecase
from dddpy.presentation.api.todo.handlers import todo_api_route_handler
from dddpy.presentation.api.todo.handlers.todo_api_route_handler import (
    TodoApiRouteHandler,
)
from dddpy.usecase.todo import CreateTodoUseCase


@pytest.fixture
def create_todo_usecase_mock():
    """Create a mock CreateTodoUseCase."""
    return Mock(spec=CreateTodoUseCase)


@pytest.fixture
def client(create_todo_usecase_mock):
    """Create a test client with the create use case overridden."""
    app = FastAPI()
    TodoApiRouteHandler().register_routes(app)
    app.dependency_overrides[get_create_todo_usecase] = lambda: create_todo_usecase_mock
    return TestClient(app)


def test_create_todo(client, create_todo_usecase_mock):
    """Test creating a todo returns 201 and passes value objects."""
    todo_id = uuid4()
    create_todo_usecase_mock.execute.return_value = Todo(
        TodoId(todo_id), TodoTitle('title'), TodoDescription('description')
    )

    response = client.post(
        '/todos', json={'title': 'title', 'description': 'description'}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['id'] == str(todo_id)
    assert response.json()['title'] == 'title'
    assert response.json()['description'] == 'description'
    create_todo_usecase_mock.execute.assert_called_once_with(
        TodoTitle('title'), TodoDescription('description')
    )


def test_create_todo_without_description(client, create_todo_usecase_mock):
    """Test omitting the description passes None to the use case."""
    create_todo_usecase_mock.execute.return_value = Todo(
        TodoId(uuid4()), TodoTitle('title')
    )

    response = client.post('/todos', json={'title': 'title'})

    assert response.status_code == status.HTTP_201_CREATED
    create_todo_usecase_mock.execute.assert_called_once_with(TodoTitle('title'), None)


@pytest.mark.parametrize(
    ('target', 'message'),
    [
        ('TodoTitle', TITLE_REQUIRED_ERROR_MESSAGE),
        ('_build_todo_description', DESCRIPTION_TOO_LONG_ERROR_MESSAGE),
    ],
)
def test_create_todo_domain_validation_error(
    client, create_todo_usecase_mock, monkeypatch, target, message
):
    """Test a domain validation error is mapped to 400.

    The request schema already rejects invalid titles and descriptions with 422,
    so the title and description builders are made to fail to exercise the 400
    mapping directly.
    """

    def raise_value_error(*_args: object) -> None:
        raise ValueError(message)

    monkeypatch.setattr(
        TodoApiRouteHandler if target.startswith('_') else todo_api_route_handler,
        target,
        raise_value_error,
    )

    response = client.post(
        '/todos', json={'title': 'title', 'description': 'description'}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': message}
    create_todo_usecase_mock.execute.assert_not_called()


def test_create_todo_empty_title_rejected_by_schema(client, create_todo_usecase_mock):
    """Test an empty title is rejected by request validation with 422."""
    response = client.post('/todos', json={'title': ''})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    create_todo_usecase_mock.execute.assert_not_called()
