"""Test cases for CreateTodoUseCaseImpl."""

from unittest.mock import Mock, patch

import pytest

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoDescription, TodoTitle
from dddpy.usecase.todo.create_todo_usecase import CreateTodoUseCaseImpl


@pytest.fixture
def todo_repository_mock():
    """Create a mock TodoRepository."""
    return Mock(spec=TodoRepository)


@pytest.fixture
def create_todo_usecase(todo_repository_mock):
    """Create a CreateTodoUseCaseImpl instance with mocked repository."""
    return CreateTodoUseCaseImpl(todo_repository_mock)


def test_create_todo_with_title_only(create_todo_usecase, todo_repository_mock):
    """Test creating a Todo with only title."""
    # Arrange
    title = TodoTitle('Test Todo')
    result = create_todo_usecase.execute(title=title)

    # Assert
    assert result.title == title
    assert result.description is None
    todo_repository_mock.save.assert_called_once_with(result)


def test_create_todo_with_title_and_description(
    create_todo_usecase, todo_repository_mock
):
    """Test creating a Todo with title and description."""
    # Arrange
    title = TodoTitle('Test Todo')
    description = TodoDescription('Test Description')
    result = create_todo_usecase.execute(title=title, description=description)

    # Assert
    assert result.title == title
    assert result.description == description
    todo_repository_mock.save.assert_called_once_with(result)


def test_create_todo_repository_error(create_todo_usecase, todo_repository_mock):
    """Test handling repository error when creating a Todo."""
    # Arrange
    title = TodoTitle('Test Todo')
    todo_repository_mock.save.side_effect = Exception('Database error')

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        create_todo_usecase.execute(title=title)
    assert str(exc_info.value) == 'Database error'
