"""Test cases for StartTodoUseCaseImpl."""

from unittest.mock import Mock, patch

import pytest

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoId, TodoStatus, TodoTitle
from dddpy.usecase.todo.start_todo_usecase import StartTodoUseCaseImpl


@pytest.fixture
def todo_repository_mock():
    """Create a mock TodoRepository."""
    return Mock(spec=TodoRepository)


@pytest.fixture
def start_todo_usecase(todo_repository_mock):
    """Create a StartTodoUseCaseImpl instance with mocked repository."""
    return StartTodoUseCaseImpl(todo_repository_mock)


@pytest.fixture
def todo():
    """Create a sample Todo for testing."""
    return Todo(
        id=TodoId.generate(),
        title=TodoTitle('Test Todo'),
        status=TodoStatus.NOT_STARTED,
    )


def test_start_todo_success(start_todo_usecase, todo_repository_mock, todo):
    """Test starting a Todo successfully."""
    # Arrange
    todo_repository_mock.find_by_id.return_value = todo

    # Act
    result = start_todo_usecase.execute(todo.id)

    # Assert
    assert result.status == TodoStatus.IN_PROGRESS
    todo_repository_mock.find_by_id.assert_called_once_with(todo.id)
    todo_repository_mock.save.assert_called_once_with(result)


def test_start_todo_not_found(start_todo_usecase, todo_repository_mock):
    """Test starting a non-existent Todo."""
    # Arrange
    todo_id = TodoId.generate()
    todo_repository_mock.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        start_todo_usecase.execute(todo_id)
    assert 'The Todo you specified does not exist' in str(exc_info.value)


def test_start_completed_todo(start_todo_usecase, todo_repository_mock, todo):
    """Test starting a completed Todo."""
    # Arrange
    todo.complete()  # Make the todo completed
    todo_repository_mock.find_by_id.return_value = todo

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        start_todo_usecase.execute(todo.id)
    assert 'The Todo is already completed' in str(exc_info.value)
