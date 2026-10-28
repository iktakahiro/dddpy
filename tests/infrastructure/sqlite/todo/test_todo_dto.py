"""Test cases for the TodoDTO persistence model."""

from datetime import UTC, datetime
from uuid import uuid4

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.value_objects import (
    TodoDescription,
    TodoId,
    TodoStatus,
    TodoTitle,
)
from dddpy.infrastructure.sqlite.todo import TodoDTO
from dddpy.presentation.api.todo.schemas.todo_schema import TodoSchema

CREATED_AT = datetime(2026, 1, 2, 3, 4, 5, 678000, tzinfo=UTC)
UPDATED_AT = datetime(2026, 1, 2, 3, 5, 6, 789000, tzinfo=UTC)
COMPLETED_AT = datetime(2026, 1, 2, 3, 6, 7, 890000, tzinfo=UTC)


def _to_millis(value: datetime) -> int:
    return round(value.timestamp() * 1000)


def test_from_entity_stores_epoch_milliseconds():
    """Test that timestamps are stored as epoch milliseconds."""
    todo = Todo(
        TodoId(uuid4()),
        TodoTitle('title'),
        TodoDescription('description'),
        TodoStatus.COMPLETED,
        CREATED_AT,
        UPDATED_AT,
        COMPLETED_AT,
    )

    dto = TodoDTO.from_entity(todo)

    assert dto.id == todo.id.value
    assert dto.title == 'title'
    assert dto.description == 'description'
    assert dto.status == 'completed'
    assert dto.created_at == _to_millis(CREATED_AT)
    assert dto.updated_at == _to_millis(UPDATED_AT)
    assert dto.completed_at == _to_millis(COMPLETED_AT)


def test_from_entity_without_optional_values():
    """Test that missing description and completion time map to None."""
    todo = Todo(TodoId(uuid4()), TodoTitle('title'), None, TodoStatus.NOT_STARTED)

    dto = TodoDTO.from_entity(todo)

    assert dto.description is None
    assert dto.status == 'not_started'
    assert dto.completed_at is None


def test_to_entity_restores_aware_utc_datetimes():
    """Test that persisted milliseconds are restored as aware UTC datetimes."""
    dto = TodoDTO(
        id=uuid4(),
        title='title',
        description=None,
        status='in_progress',
        created_at=_to_millis(CREATED_AT),
        updated_at=_to_millis(UPDATED_AT),
        completed_at=None,
    )

    todo = dto.to_entity()

    assert todo.id.value == dto.id
    assert todo.status == TodoStatus.IN_PROGRESS
    assert todo.description is None
    assert todo.created_at == CREATED_AT
    assert todo.created_at.tzinfo is UTC
    assert todo.updated_at == UPDATED_AT
    assert todo.completed_at is None


def test_dto_round_trip_preserves_timestamps_and_overdue_comparison():
    """Test UTC timestamps survive conversion and can be compared."""
    todo = Todo(
        TodoId(uuid4()),
        TodoTitle('title'),
        created_at=CREATED_AT,
        updated_at=UPDATED_AT,
        completed_at=COMPLETED_AT,
    )
    restored = TodoDTO.from_entity(todo).to_entity()
    assert restored.created_at == CREATED_AT
    assert restored.updated_at == UPDATED_AT
    assert restored.completed_at == COMPLETED_AT
    assert restored.is_overdue(restored.created_at)


def test_epoch_completion_round_trips_to_entity_and_response():
    """Test an epoch completion timestamp remains zero across conversions."""
    dto = TodoDTO(
        id=uuid4(),
        title='title',
        description=None,
        status='completed',
        created_at=0,
        updated_at=0,
        completed_at=0,
    )
    todo = dto.to_entity()
    assert todo.completed_at == datetime(1970, 1, 1, tzinfo=UTC)
    assert TodoDTO.from_entity(todo).completed_at == 0
    assert TodoSchema.from_entity(todo).completed_at == 0
