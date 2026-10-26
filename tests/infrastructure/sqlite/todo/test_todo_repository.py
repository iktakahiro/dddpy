"""Integration tests for TodoRepositoryImpl against in-memory SQLite."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from dddpy.domain.todo.entities import Todo
from dddpy.domain.todo.value_objects import (
    TodoDescription,
    TodoId,
    TodoStatus,
    TodoTitle,
)
from dddpy.infrastructure.sqlite.todo import TodoDTO, TodoRepositoryImpl

BASE_TIME = datetime(2026, 1, 2, 3, 4, 5, 123000, tzinfo=UTC)
FIND_ALL_LIMIT = 20
OVER_LIMIT_COUNT = 25


@pytest.fixture
def repository(session: Session) -> TodoRepositoryImpl:
    """Return a repository bound to the in-memory session."""
    return TodoRepositoryImpl(session)


def _make_todo(
    title: str = 'title',
    description: str | None = 'description',
    created_at: datetime = BASE_TIME,
) -> Todo:
    return Todo(
        TodoId(uuid4()),
        TodoTitle(title),
        TodoDescription(description) if description is not None else None,
        TodoStatus.NOT_STARTED,
        created_at,
        created_at,
    )


def _millis(value: datetime | None) -> int | None:
    # Compare instants: the entity uses naive local time, the DTO restores aware UTC.
    return None if value is None else round(value.timestamp() * 1000)


def _count_rows(session: Session) -> int:
    return session.scalar(select(func.count()).select_from(TodoDTO)) or 0


def _commit(session: Session) -> None:
    """Flush pending changes and drop cached state so reads hit the database."""
    session.commit()
    session.expire_all()


def test_save_inserts_new_todo_and_find_by_id_restores_it(
    repository: TodoRepositoryImpl, session: Session
):
    """Test that a saved todo is persisted and restored with identical values."""
    todo = _make_todo()
    todo.updated_at = BASE_TIME + timedelta(milliseconds=456)

    repository.save(todo)
    _commit(session)

    found = repository.find_by_id(todo.id)

    assert found is not None
    assert found.id == todo.id
    assert found.title == todo.title
    assert found.description == todo.description
    assert found.status == TodoStatus.NOT_STARTED
    assert _millis(found.created_at) == _millis(todo.created_at)
    assert _millis(found.updated_at) == _millis(todo.updated_at)
    assert found.completed_at is None
    assert _count_rows(session) == 1


def test_find_by_id_returns_a_new_entity_from_the_database(
    repository: TodoRepositoryImpl, session: Session
):
    """Test that the entity is rebuilt from the row, not reused from memory."""
    todo = _make_todo()
    repository.save(todo)
    _commit(session)

    found = repository.find_by_id(todo.id)

    assert found is not None
    assert found.id == todo.id
    assert found is not todo


def test_save_naive_local_datetimes_round_trip_as_same_instant(
    repository: TodoRepositoryImpl, session: Session
):
    """Test that naive datetimes, as produced by Todo.create, keep their instant."""
    naive = datetime(2026, 3, 4, 5, 6, 7, 891000)
    todo = _make_todo(created_at=naive)
    todo.complete()
    todo.completed_at = naive + timedelta(seconds=1)
    todo.updated_at = todo.completed_at

    repository.save(todo)
    _commit(session)
    found = repository.find_by_id(todo.id)

    assert found is not None
    assert found.created_at.tzinfo is not None
    assert _millis(found.created_at) == _millis(todo.created_at)
    assert _millis(found.updated_at) == _millis(todo.updated_at)
    assert _millis(found.completed_at) == _millis(todo.completed_at)


def test_find_by_id_returns_none_for_unknown_id(repository: TodoRepositoryImpl):
    """Test that an unknown identifier yields None."""
    assert repository.find_by_id(TodoId(uuid4())) is None


def test_find_by_id_does_not_return_other_todos(
    repository: TodoRepositoryImpl, session: Session
):
    """Test that lookups only match the requested identifier."""
    first = _make_todo('first')
    second = _make_todo('second')
    repository.save(first)
    repository.save(second)
    _commit(session)

    found = repository.find_by_id(second.id)

    assert found is not None
    assert found.title == TodoTitle('second')


def test_save_existing_todo_updates_row_without_duplicating(
    repository: TodoRepositoryImpl, session: Session
):
    """Test that saving a known id updates the mutable columns in place."""
    todo = _make_todo('old title', 'old description')
    repository.save(todo)
    _commit(session)

    changed = Todo(
        todo.id,
        TodoTitle('new title'),
        TodoDescription('new description'),
        TodoStatus.COMPLETED,
        BASE_TIME + timedelta(days=5),  # created_at must not be overwritten
        BASE_TIME + timedelta(hours=1, milliseconds=7),
        BASE_TIME + timedelta(hours=1, milliseconds=7),
    )
    repository.save(changed)
    _commit(session)

    found = repository.find_by_id(todo.id)

    assert _count_rows(session) == 1
    assert found is not None
    assert found.title == TodoTitle('new title')
    assert found.description == TodoDescription('new description')
    assert found.status == TodoStatus.COMPLETED
    assert _millis(found.created_at) == _millis(BASE_TIME)
    assert _millis(found.updated_at) == _millis(changed.updated_at)
    assert _millis(found.completed_at) == _millis(changed.completed_at)


def test_save_existing_todo_can_clear_description(
    repository: TodoRepositoryImpl, session: Session
):
    """Test that updating with no description stores NULL."""
    todo = _make_todo(description='to be removed')
    repository.save(todo)
    _commit(session)

    todo.update_description(None)
    repository.save(todo)
    _commit(session)

    found = repository.find_by_id(todo.id)

    assert found is not None
    assert found.description is None
    assert _count_rows(session) == 1


def test_save_is_visible_to_queries_before_commit(
    repository: TodoRepositoryImpl, session: Session
):
    """Test that autoflush makes an unsaved-but-added todo queryable."""
    todo = _make_todo()

    repository.save(todo)

    assert repository.find_by_id(todo.id) is not None


def test_description_none_round_trip(repository: TodoRepositoryImpl, session: Session):
    """Test that a todo without a description is stored as NULL and restored."""
    todo = _make_todo(description=None)

    repository.save(todo)
    _commit(session)

    row = session.get(TodoDTO, todo.id.value)
    found = repository.find_by_id(todo.id)

    assert row is not None
    assert row.description is None
    assert found is not None
    assert found.description is None


def test_completed_todo_round_trip(repository: TodoRepositoryImpl, session: Session):
    """Test that status and completed_at survive persistence."""
    todo = _make_todo()
    todo.status = TodoStatus.COMPLETED
    todo.completed_at = BASE_TIME + timedelta(minutes=3, milliseconds=21)
    todo.updated_at = todo.completed_at

    repository.save(todo)
    _commit(session)
    found = repository.find_by_id(todo.id)

    assert found is not None
    assert found.status == TodoStatus.COMPLETED
    assert found.is_completed
    assert found.completed_at is not None
    assert _millis(found.completed_at) == _millis(todo.completed_at)
    assert _millis(found.updated_at) == _millis(todo.updated_at)


def test_find_all_returns_empty_list_when_no_todos(repository: TodoRepositoryImpl):
    """Test that an empty table yields an empty list."""
    assert repository.find_all() == []


def test_find_all_returns_newest_first(
    repository: TodoRepositoryImpl, session: Session
):
    """Test that todos are ordered by created_at in descending order."""
    oldest = _make_todo('oldest', created_at=BASE_TIME)
    newest = _make_todo('newest', created_at=BASE_TIME + timedelta(minutes=2))
    middle = _make_todo('middle', created_at=BASE_TIME + timedelta(minutes=1))
    for todo in (oldest, newest, middle):
        repository.save(todo)
    _commit(session)

    titles = [todo.title.value for todo in repository.find_all()]

    assert titles == ['newest', 'middle', 'oldest']


def test_find_all_returns_at_most_twenty_newest_todos(
    repository: TodoRepositoryImpl, session: Session
):
    """Test that the result is capped at 20 items, keeping the newest ones."""
    for index in range(OVER_LIMIT_COUNT):
        repository.save(
            _make_todo(f'todo {index}', created_at=BASE_TIME + timedelta(seconds=index))
        )
    _commit(session)

    todos = repository.find_all()

    assert _count_rows(session) == OVER_LIMIT_COUNT
    assert len(todos) == FIND_ALL_LIMIT
    assert [todo.title.value for todo in todos] == [
        f'todo {index}'
        for index in range(
            OVER_LIMIT_COUNT - 1, OVER_LIMIT_COUNT - 1 - FIND_ALL_LIMIT, -1
        )
    ]


def test_delete_removes_the_row(repository: TodoRepositoryImpl, session: Session):
    """Test that delete removes only the requested todo."""
    target = _make_todo('target')
    keeper = _make_todo('keeper')
    repository.save(target)
    repository.save(keeper)
    _commit(session)

    repository.delete(target.id)
    _commit(session)

    assert repository.find_by_id(target.id) is None
    assert repository.find_by_id(keeper.id) is not None
    assert _count_rows(session) == 1


def test_delete_unknown_id_is_a_no_op(repository: TodoRepositoryImpl, session: Session):
    """Test that deleting a missing todo neither raises nor removes other rows."""
    todo = _make_todo()
    repository.save(todo)
    _commit(session)

    repository.delete(TodoId(uuid4()))
    _commit(session)

    assert _count_rows(session) == 1
    assert repository.find_by_id(todo.id) is not None


def test_delete_pending_todo_hides_it_from_the_session(
    repository: TodoRepositoryImpl, session: Session
):
    """Test that a todo deleted in the same transaction is no longer found."""
    todo = _make_todo()
    repository.save(todo)
    _commit(session)
    assert repository.find_by_id(todo.id) is not None

    repository.delete(todo.id)

    assert repository.find_by_id(todo.id) is None
