"""Test request body validation for todo creation and updates."""

from collections.abc import Iterator
from uuid import uuid4

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from dddpy.infrastructure.di.injection import get_session
from dddpy.infrastructure.sqlite.database import Base
from dddpy.infrastructure.sqlite.todo import TodoDTO  # noqa: F401  # registers the model
from dddpy.presentation.api.todo.handlers.todo_api_route_handler import (
    TodoApiRouteHandler,
)


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Yield a test client backed by an isolated SQLite database."""
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)

    def override_session() -> Iterator[Session]:
        with Session(engine) as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise

    app = FastAPI()
    TodoApiRouteHandler().register_routes(app)
    app.dependency_overrides[get_session] = override_session
    with TestClient(app) as test_client:
        yield test_client
    engine.dispose()


@pytest.mark.parametrize('method', ['POST', 'PUT'])
@pytest.mark.parametrize(
    ('content', 'error_type'),
    [(None, 'missing'), ('null', 'model_attributes_type')],
)
def test_missing_and_null_bodies(client, method, content, error_type):
    """Distinguish omitted request bodies from literal JSON null."""
    path = '/todos' if method == 'POST' else f'/todos/{uuid4()}'
    response = client.request(
        method, path, content=content, headers={'content-type': 'application/json'}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()['detail'][0]['type'] == error_type
    assert response.json()['detail'][0]['loc'] == ['body']


@pytest.mark.parametrize('method', ['POST', 'PUT'])
def test_null_description(client, method):
    """Accept a null description when creating or updating a todo."""
    path = '/todos'
    if method == 'PUT':
        created = client.post(path, json={'title': 'Original', 'description': 'Text'})
        assert created.status_code == status.HTTP_201_CREATED
        path = f'/todos/{created.json()["id"]}'

    response = client.request(
        method, path, json={'title': 'Updated', 'description': None}
    )

    expected_status = (
        status.HTTP_201_CREATED if method == 'POST' else status.HTTP_200_OK
    )
    assert response.status_code == expected_status
    assert response.json()['title'] == 'Updated'
    assert response.json()['description'] == ('' if method == 'POST' else 'Text')
