"""Test cases for the TodoSchema response model."""

from datetime import UTC, datetime

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.value_objects import TodoId, TodoStatus, TodoTitle
from dddpy.presentation.api.todo.schemas.todo_schema import TodoSchema

CREATED_AT_MS = 1767323045678
UPDATED_AT_MS = 1767323106789
COMPLETED_AT_MS = 1767323167890


def test_from_entity_serializes_epoch_milliseconds():
    """Test timestamps are serialized as epoch milliseconds."""
    todo = Todo(
        TodoId.generate(),
        TodoTitle('title'),
        status=TodoStatus.COMPLETED,
        created_at=datetime(2026, 1, 2, 3, 4, 5, 678000, tzinfo=UTC),
        updated_at=datetime(2026, 1, 2, 3, 5, 6, 789000, tzinfo=UTC),
        completed_at=datetime(2026, 1, 2, 3, 6, 7, 890000, tzinfo=UTC),
    )

    schema = TodoSchema.from_entity(todo)

    assert schema.created_at == CREATED_AT_MS
    assert schema.updated_at == UPDATED_AT_MS
    assert schema.completed_at == COMPLETED_AT_MS


def test_from_entity_keeps_epoch_zero_completion_timestamp():
    """Test an epoch-zero completion timestamp is not treated as missing."""
    epoch = datetime(1970, 1, 1, tzinfo=UTC)
    todo = Todo(
        TodoId.generate(),
        TodoTitle('title'),
        status=TodoStatus.COMPLETED,
        created_at=epoch,
        updated_at=epoch,
        completed_at=epoch,
    )

    assert TodoSchema.from_entity(todo).completed_at == 0


def test_from_entity_without_completion_timestamp():
    """Test a todo without completion time serializes completed_at as None."""
    todo = Todo.create(TodoTitle('title'))
    assert TodoSchema.from_entity(todo).completed_at is None
