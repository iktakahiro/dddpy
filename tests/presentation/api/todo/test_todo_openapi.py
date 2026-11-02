"""Test cases for the OpenAPI schema of the todo routes."""

import pytest
from fastapi import FastAPI

from dddpy.domain.todo.exceptions import (
    TodoAlreadyCompletedError,
    TodoAlreadyStartedError,
    TodoNotStartedError,
)
from dddpy.domain.todo.value_objects.todo_description import (
    DESCRIPTION_TOO_LONG_ERROR_MESSAGE,
)
from dddpy.domain.todo.value_objects.todo_title import (
    TITLE_REQUIRED_ERROR_MESSAGE,
    TITLE_TOO_LONG_ERROR_MESSAGE,
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


def _example_details(response):
    """Collect the ``detail`` values of every example in a JSON response."""
    examples = response['content']['application/json']['examples']
    return {e['value']['detail'] for e in examples.values()}


def _ref_names(schema):
    """Collect the model names referenced by a schema, directly or via anyOf."""
    refs = schema['anyOf'] if 'anyOf' in schema else [schema]
    return {ref['$ref'].rsplit('/', 1)[-1] for ref in refs}


@pytest.mark.parametrize(
    ('path', 'method', 'expected_models', 'expected_messages'),
    [
        (
            '/todos/{todo_id}/start',
            'patch',
            {'ErrorMessageTodoAlreadyStarted', 'ErrorMessageTodoAlreadyCompleted'},
            {TodoAlreadyStartedError.message, TodoAlreadyCompletedError.message},
        ),
        (
            '/todos/{todo_id}/complete',
            'patch',
            {'ErrorMessageTodoNotStarted', 'ErrorMessageTodoAlreadyCompleted'},
            {TodoNotStartedError.message, TodoAlreadyCompletedError.message},
        ),
    ],
)
def test_lifecycle_routes_document_400(
    openapi_schema, path, method, expected_models, expected_messages
):
    """Test lifecycle routes list 400 models and messages and keep the 404."""
    responses = openapi_schema['paths'][path][method]['responses']

    assert '404' in responses
    assert (
        _ref_names(responses['400']['content']['application/json']['schema'])
        == expected_models
    )
    assert _example_details(responses['400']) == expected_messages


@pytest.mark.parametrize(
    ('path', 'method'),
    [('/todos', 'post'), ('/todos/{todo_id}', 'put')],
)
def test_write_routes_document_400(openapi_schema, path, method):
    """Test create and update routes list a 400 model and every domain message."""
    response = openapi_schema['paths'][path][method]['responses']['400']

    assert _ref_names(response['content']['application/json']['schema']) == {
        'ErrorMessageInvalidTodo'
    }
    assert _example_details(response) == {
        TITLE_REQUIRED_ERROR_MESSAGE,
        TITLE_TOO_LONG_ERROR_MESSAGE,
        DESCRIPTION_TOO_LONG_ERROR_MESSAGE,
    }
