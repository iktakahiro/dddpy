"""Test cases for CompleteTodoUseCaseImpl."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoId, TodoStatus, TodoTitle
from dddpy.usecase.todo.complete_todo_usecase import CompleteTodoUseCaseImpl


@pytest.fixture
def todo_repository_mock():
    """Create a mock TodoRepository."""
    return Mock(spec=TodoRepository)


@pytest.fixture
def complete_todo_usecase(todo_repository_mock):
    """Create a CompleteTodoUseCaseImpl instance with mocked repository."""
    return CompleteTodoUseCaseImpl(todo_repository_mock)


@pytest.fixture
def todo():
    """Create a sample Todo for testing."""
    todo = Todo(
        id=TodoId.generate(),
        title=TodoTitle('Test Todo'),
        status=TodoStatus.NOT_STARTED,
    )
    todo.start()  # Set the todo to IN_PROGRESS state
    return todo


def test_complete_todo_success(complete_todo_usecase, todo_repository_mock, todo):
    """Test completing a Todo successfully."""
    # Arrange
    todo_repository_mock.find_by_id.return_value = todo

    # Act
    result = complete_todo_usecase.execute(todo.id)

    # Assert
    assert result.status == TodoStatus.COMPLETED
    assert result.completed_at is not None
    todo_repository_mock.find_by_id.assert_called_once_with(todo.id)
    todo_repository_mock.save.assert_called_once_with(result)


def test_complete_todo_not_found(complete_todo_usecase, todo_repository_mock):
    """Test completing a non-existent Todo."""
    # Arrange
    todo_id = TodoId.generate()
    todo_repository_mock.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        complete_todo_usecase.execute(todo_id)
    assert 'The Todo you specified does not exist' in str(exc_info.value)


def test_complete_already_completed_todo(
    complete_todo_usecase, todo_repository_mock, todo
):
    """Test completing an already completed Todo."""
    # Arrange
    todo.complete()  # Make the todo completed
    todo_repository_mock.find_by_id.return_value = todo

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        complete_todo_usecase.execute(todo.id)
    assert 'The Todo is already completed' in str(exc_info.value)
