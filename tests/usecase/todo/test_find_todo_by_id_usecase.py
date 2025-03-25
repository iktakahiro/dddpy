"""Test cases for FindTodoByIdUseCaseImpl."""

from unittest.mock import Mock, patch

import pytest

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoDescription, TodoId, TodoTitle
from dddpy.usecase.todo.find_todo_by_id_usecase import FindTodoByIdUseCaseImpl


@pytest.fixture
def todo_repository_mock():
    """Create a mock TodoRepository."""
    return Mock(spec=TodoRepository)


@pytest.fixture
def find_todo_by_id_usecase(todo_repository_mock):
    """Create a FindTodoByIdUseCaseImpl instance with mocked repository."""
    return FindTodoByIdUseCaseImpl(todo_repository_mock)


@pytest.fixture
def todo():
    """Create a sample Todo for testing."""
    return Todo(
        id=TodoId.generate(),
        title=TodoTitle('Test Todo'),
        description=TodoDescription('Test Description'),
    )


def test_find_todo_by_id_success(find_todo_by_id_usecase, todo_repository_mock, todo):
    """Test finding a Todo by ID successfully."""
    # Arrange
    todo_repository_mock.find_by_id.return_value = todo

    # Act
    result = find_todo_by_id_usecase.execute(todo.id)

    # Assert
    assert result == todo
    todo_repository_mock.find_by_id.assert_called_once_with(todo.id)


def test_find_todo_by_id_not_found(find_todo_by_id_usecase, todo_repository_mock):
    """Test finding a non-existent Todo by ID."""
    # Arrange
    todo_id = TodoId.generate()
    todo_repository_mock.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        find_todo_by_id_usecase.execute(todo_id)
    assert 'The Todo you specified does not exist' in str(exc_info.value)
