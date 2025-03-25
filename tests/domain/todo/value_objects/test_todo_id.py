"""Tests for TodoId value object."""

from uuid import UUID

import pytest

from dddpy.domain.todo.value_objects.todo_id import TodoId


def test_generate_creates_valid_uuid():
    """Test that generate() creates a valid UUID."""
    todo_id = TodoId.generate()
    assert isinstance(todo_id.value, UUID)
    assert todo_id.value.version == 4  # Check if it's a UUID4


def test_generate_creates_unique_ids():
    """Test that generate() creates unique IDs."""
    id1 = TodoId.generate()
    id2 = TodoId.generate()
    assert id1.value != id2.value


def test_str_representation():
    """Test the string representation of TodoId."""
    todo_id = TodoId.generate()
    assert str(todo_id) == str(todo_id.value)
