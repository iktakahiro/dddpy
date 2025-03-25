"""Test cases for FindTodosUseCaseImpl."""

from unittest.mock import Mock, patch

import pytest

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoDescription, TodoId, TodoTitle
from dddpy.usecase.todo.find_todos_usecase import FindTodosUseCaseImpl


@pytest.fixture
def todo_repository_mock():
    """Create a mock TodoRepository."""
    return Mock(spec=TodoRepository)


@pytest.fixture
def find_todos_usecase(todo_repository_mock):
    """Create a FindTodosUseCaseImpl instance with mocked repository."""
    return FindTodosUseCaseImpl(todo_repository_mock)


def test_find_todos_empty_list(find_todos_usecase, todo_repository_mock):
    """Test finding todos when there are no todos."""
    # Arrange
    todo_repository_mock.find_all.return_value = []

    # Act
    result = find_todos_usecase.execute()

    # Assert
    assert len(result) == 0
    todo_repository_mock.find_all.assert_called_once()


def test_find_todos_with_items(find_todos_usecase, todo_repository_mock):
    """Test finding todos when there are todos in the repository."""
    # Arrange
    todos = [
        Todo(
            id=TodoId.generate(),
            title=TodoTitle('Todo 1'),
            description=TodoDescription('Description 1'),
        ),
        Todo(
            id=TodoId.generate(),
            title=TodoTitle('Todo 2'),
            description=TodoDescription('Description 2'),
        ),
    ]
    todo_repository_mock.find_all.return_value = todos

    # Act
    result = find_todos_usecase.execute()

    # Assert
    assert len(result) == 2
    assert result[0].title == todos[0].title
    assert result[1].title == todos[1].title
    todo_repository_mock.find_all.assert_called_once()
