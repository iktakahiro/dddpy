"""Tests for TodoStatus value object."""

from dddpy.domain.todo.value_objects.todo_status import TodoStatus


def test_todo_status_values():
    """Test that TodoStatus has the correct values."""
    assert TodoStatus.NOT_STARTED.value == "not_started"
    assert TodoStatus.IN_PROGRESS.value == "in_progress"
    assert TodoStatus.COMPLETED.value == "completed"


def test_todo_status_enum_members():
    """Test that TodoStatus has the correct enum members."""
    assert len(TodoStatus) == 3
    assert TodoStatus.NOT_STARTED in TodoStatus
    assert TodoStatus.IN_PROGRESS in TodoStatus
    assert TodoStatus.COMPLETED in TodoStatus


def test_str_representation():
    """Test the string representation of TodoStatus."""
    assert str(TodoStatus.NOT_STARTED) == "not_started"
    assert str(TodoStatus.IN_PROGRESS) == "in_progress"
    assert str(TodoStatus.COMPLETED) == "completed" 