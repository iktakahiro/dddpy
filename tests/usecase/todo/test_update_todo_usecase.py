"""Test cases for UpdateTodoUseCaseImpl."""

from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.exceptions import TodoNotFoundError
from dddpy.domain.todo.repositories import TodoRepository
from dddpy.domain.todo.value_objects import TodoDescription, TodoId, TodoTitle
from dddpy.usecase.todo.update_todo_usecase import (
    UpdateTodoUseCaseImpl,
    new_update_todo_usecase,
)

OLD_TIMESTAMP = datetime(2020, 1, 1, tzinfo=UTC)


@pytest.fixture
def todo_repository_mock():
    """Create a mock TodoRepository."""
    return Mock(spec=TodoRepository)


@pytest.fixture
def update_todo_usecase(todo_repository_mock):
    """Create a UpdateTodoUseCaseImpl instance with mocked repository."""
    return UpdateTodoUseCaseImpl(todo_repository_mock)


@pytest.fixture
def todo():
    """Create a sample Todo for testing."""
    return Todo(
        id=TodoId.generate(),
        title=TodoTitle('Original Title'),
        description=TodoDescription('Original Description'),
        created_at=OLD_TIMESTAMP,
        updated_at=OLD_TIMESTAMP,
    )


def test_update_todo_title_only(update_todo_usecase, todo_repository_mock, todo):
    """Test updating a Todo's title only."""
    # Arrange
    todo_repository_mock.find_by_id.return_value = todo
    original_description = todo.description
    new_title = TodoTitle('Updated Title')

    # Act
    result = update_todo_usecase.execute(todo.id, title=new_title)

    # Assert
    assert result.title == new_title
    assert result.description == original_description
    assert result.updated_at > OLD_TIMESTAMP
    todo_repository_mock.find_by_id.assert_called_once_with(todo.id)
    todo_repository_mock.save.assert_called_once_with(result)


def test_update_todo_description_only(update_todo_usecase, todo_repository_mock, todo):
    """Test updating a Todo's description only."""
    # Arrange
    todo_repository_mock.find_by_id.return_value = todo
    original_title = todo.title
    new_description = TodoDescription('Updated Description')

    # Act
    result = update_todo_usecase.execute(todo.id, description=new_description)

    # Assert
    assert result.title == original_title
    assert result.description == new_description
    assert result.updated_at > OLD_TIMESTAMP
    todo_repository_mock.find_by_id.assert_called_once_with(todo.id)
    todo_repository_mock.save.assert_called_once_with(result)


def test_update_todo_both_fields(update_todo_usecase, todo_repository_mock, todo):
    """Test updating both title and description of a Todo."""
    # Arrange
    todo_repository_mock.find_by_id.return_value = todo
    new_title = TodoTitle('Updated Title')
    new_description = TodoDescription('Updated Description')

    # Act
    result = update_todo_usecase.execute(
        todo.id, title=new_title, description=new_description
    )

    # Assert
    assert result.title == new_title
    assert result.description == new_description
    assert result.updated_at > OLD_TIMESTAMP
    todo_repository_mock.find_by_id.assert_called_once_with(todo.id)
    todo_repository_mock.save.assert_called_once_with(result)


def test_update_todo_neither_field(update_todo_usecase, todo_repository_mock, todo):
    """Test updating a Todo without any values keeps it unchanged but saves it."""
    # Arrange
    todo_repository_mock.find_by_id.return_value = todo
    original_title = todo.title
    original_description = todo.description

    # Act
    result = update_todo_usecase.execute(todo.id)

    # Assert
    assert result.title == original_title
    assert result.description == original_description
    # The entity's update methods are not called, so the timestamp is untouched.
    assert result.updated_at == OLD_TIMESTAMP
    todo_repository_mock.find_by_id.assert_called_once_with(todo.id)
    todo_repository_mock.save.assert_called_once_with(result)


def test_update_todo_not_found(update_todo_usecase, todo_repository_mock):
    """Test updating a non-existent Todo."""
    # Arrange
    todo_id = TodoId.generate()
    todo_repository_mock.find_by_id.return_value = None
    new_title = TodoTitle('Updated Title')

    # Act & Assert
    with pytest.raises(TodoNotFoundError) as exc_info:
        update_todo_usecase.execute(todo_id, title=new_title)
    assert 'The Todo you specified does not exist' in str(exc_info.value)
    todo_repository_mock.find_by_id.assert_called_once_with(todo_id)
    todo_repository_mock.save.assert_not_called()


def test_new_update_todo_usecase(todo_repository_mock, todo):
    """Test the factory returns a working use case bound to the repository."""
    # Arrange
    todo_repository_mock.find_by_id.return_value = todo
    new_title = TodoTitle('Updated Title')

    # Act
    usecase = new_update_todo_usecase(todo_repository_mock)
    result = usecase.execute(todo.id, title=new_title)

    # Assert
    assert isinstance(usecase, UpdateTodoUseCaseImpl)
    assert result.title == new_title
    todo_repository_mock.save.assert_called_once_with(result)
