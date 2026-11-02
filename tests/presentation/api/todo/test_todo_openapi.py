"""Test cases for the OpenAPI schema of the todo routes."""

import pytest
from fastapi import FastAPI

from dddpy.domain.todo.exceptions import (
    TodoAlreadyCompletedError,
    TodoAlreadyStartedError,
    TodoNotStartedError,
)
from dddpy.presentation.api.todo.handlers.todo_api_route_handler import (
    TodoApiRouteHandler,
)


@pytest.fixture
def openapi_schema():
    """Build the OpenAPI schema of an app with the todo routes."""
    app = FastAPI()
    TodoApiRouteHandler().register_routes(app)
    return app.openapi()


@pytest.mark.parametrize(
    ('path', 'method', 'expected_messages'),
    [
        (
            '/todos/{todo_id}/start',
            'patch',
            {TodoAlreadyStartedError.message, TodoAlreadyCompletedError.message},
        ),
        (
            '/todos/{todo_id}/complete',
            'patch',
            {TodoNotStartedError.message, TodoAlreadyCompletedError.message},
        ),
    ],
)
def test_lifecycle_routes_document_400(openapi_schema, path, method, expected_messages):
    """Test lifecycle routes list a 400 response with every possible message."""
    response = openapi_schema['paths'][path][method]['responses']['400']

    examples = response['content']['application/json']['examples']
    assert {e['value']['detail'] for e in examples.values()} == expected_messages


@pytest.mark.parametrize(
    ('path', 'method'),
    [('/todos', 'post'), ('/todos/{todo_id}', 'put')],
)
def test_write_routes_document_400(openapi_schema, path, method):
    """Test create and update routes list a described 400 response."""
    response = openapi_schema['paths'][path][method]['responses']['400']

    assert response['description'] != 'Bad Request'
