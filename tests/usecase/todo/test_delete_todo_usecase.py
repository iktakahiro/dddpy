"""Test cases for DeleteTodoUseCaseImpl."""

from unittest.mock import Mock, patch

import pytest

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoId, TodoTitle
from dddpy.usecase.todo.delete_todo_usecase import DeleteTodoUseCaseImpl


@pytest.fixture
def todo_repository_mock():
    """Create a mock TodoRepository."""
    return Mock(spec=TodoRepository)


@pytest.fixture
def delete_todo_usecase(todo_repository_mock):
    """Create a DeleteTodoUseCaseImpl instance with mocked repository."""
    return DeleteTodoUseCaseImpl(todo_repository_mock)


@pytest.fixture
def todo():
    """Create a sample Todo for testing."""
    return Todo(
        id=TodoId.generate(),
        title=TodoTitle('Test Todo'),
    )


def test_delete_todo_success(delete_todo_usecase, todo_repository_mock, todo):
    """Test deleting a Todo successfully."""
    # Arrange
    todo_repository_mock.find_by_id.return_value = todo

    # Act
    delete_todo_usecase.execute(todo.id)

    # Assert
    todo_repository_mock.find_by_id.assert_called_once_with(todo.id)
    todo_repository_mock.delete.assert_called_once_with(todo.id)


def test_delete_todo_not_found(delete_todo_usecase, todo_repository_mock):
    """Test deleting a non-existent Todo."""
    # Arrange
    todo_id = TodoId.generate()
    todo_repository_mock.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        delete_todo_usecase.execute(todo_id)
    assert 'The Todo you specified does not exist' in str(exc_info.value)
