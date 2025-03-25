"""Test cases for the Todo entity."""

from datetime import datetime, timedelta

import pytest

from dddpy.domain.todo.entities.todo import Todo
from dddpy.domain.todo.value_objects import (
    TodoDescription,
    TodoId,
    TodoStatus,
    TodoTitle,
)


def test_create_todo():
    """Test creating a new Todo."""
    title = TodoTitle('Test Todo')
    description = TodoDescription('Test Description')
    todo = Todo.create(title, description)

    assert isinstance(todo.id, TodoId)
    assert todo.title == title
    assert todo.description == description
    assert todo.status == TodoStatus.NOT_STARTED
    assert isinstance(todo.created_at, datetime)
    assert isinstance(todo.updated_at, datetime)
    assert todo.completed_at is None


def test_todo_properties():
    """Test Todo properties."""
    todo_id = TodoId.generate()
    title = TodoTitle('Test Todo')
    description = TodoDescription('Test Description')
    created_at = datetime.now()
    updated_at = datetime.now()

    todo = Todo(
        id=todo_id,
        title=title,
        description=description,
        status=TodoStatus.NOT_STARTED,
        created_at=created_at,
        updated_at=updated_at,
    )

    assert todo.id == todo_id
    assert todo.title == title
    assert todo.description == description
    assert todo.status == TodoStatus.NOT_STARTED
    assert todo.created_at == created_at
    assert todo.updated_at == updated_at
    assert todo.completed_at is None


def test_update_title():
    """Test updating Todo title."""
    todo = Todo.create(TodoTitle('Original Title'))
    new_title = TodoTitle('Updated Title')

    todo.update_title(new_title)

    assert todo.title == new_title
    assert todo.updated_at > todo.created_at


def test_update_description():
    """Test updating Todo description."""
    todo = Todo.create(TodoTitle('Test Todo'))
    new_description = TodoDescription('Updated Description')

    todo.update_description(new_description)

    assert todo.description == new_description
    assert todo.updated_at > todo.created_at


def test_clear_description():
    """Test clearing Todo description."""
    todo = Todo.create(TodoTitle('Test Todo'), TodoDescription('Original Description'))

    todo.update_description(None)

    assert todo.description is None
    assert todo.updated_at > todo.created_at


def test_start_todo():
    """Test starting a Todo."""
    todo = Todo.create(TodoTitle('Test Todo'))

    todo.start()

    assert todo.status == TodoStatus.IN_PROGRESS
    assert todo.updated_at > todo.created_at


def test_complete_todo():
    """Test completing a Todo."""
    todo = Todo.create(TodoTitle('Test Todo'))

    todo.complete()

    assert todo.status == TodoStatus.COMPLETED
    assert todo.is_completed
    assert todo.completed_at is not None
    assert todo.updated_at == todo.completed_at


def test_complete_already_completed_todo():
    """Test attempting to complete an already completed Todo."""
    todo = Todo.create(TodoTitle('Test Todo'))
    todo.complete()

    with pytest.raises(ValueError, match='Already completed'):
        todo.complete()


def test_is_overdue():
    """Test checking if a Todo is overdue."""
    # Create a todo with specific timestamps
    created_at = datetime(2025, 3, 22)  # 2 days before deadline
    deadline = datetime(2025, 3, 24)  # deadline
    current_time = datetime(2025, 3, 23)  # 1 day before deadline

    # Test case 1: Not completed todo should not be overdue before deadline
    todo = Todo(
        id=TodoId.generate(),
        title=TodoTitle('Test Todo'),
        created_at=created_at,
        updated_at=created_at,
    )
    assert not todo.is_overdue(deadline, current_time)

    # Test case 2: Not completed todo should be overdue after deadline
    current_time = datetime(2025, 3, 25)  # 1 day after deadline
    assert todo.is_overdue(deadline, current_time)

    # Test case 3: Completed todo should never be overdue, even if completed after deadline
    todo.complete()
    assert not todo.is_overdue(deadline, current_time)

    # Test case 4: Completed todo should never be overdue when completed before deadline
    todo = Todo(
        id=TodoId.generate(),
        title=TodoTitle('Test Todo'),
        created_at=created_at,
        updated_at=created_at,
    )
    todo.complete()
    assert not todo.is_overdue(deadline, current_time)


def test_todo_equality():
    """Test Todo equality comparison."""
    todo_id = TodoId.generate()
    todo1 = Todo.create(TodoTitle('Test Todo'))
    todo2 = Todo.create(TodoTitle('Test Todo'))
    todo3 = Todo(
        id=todo_id,
        title=TodoTitle('Test Todo'),
        status=TodoStatus.NOT_STARTED,
    )
    todo4 = Todo(
        id=todo_id,
        title=TodoTitle('Different Title'),
        status=TodoStatus.NOT_STARTED,
    )

    assert todo1 != todo2  # Different IDs
    assert todo3 == todo4  # Same ID, different titles
    assert todo1 != 'not a todo'  # Different type
