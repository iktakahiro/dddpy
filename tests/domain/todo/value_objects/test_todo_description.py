"""Tests for TodoDescription value object."""

import pytest

from dddpy.domain.todo.value_objects.todo_description import TodoDescription


def test_create_valid_description():
    """Test that a valid description can be created."""
    description = TodoDescription('Test description')
    assert description.value == 'Test description'


def test_create_description_exceeding_length_limit():
    """Test that creating a description exceeding 1000 characters raises ValueError."""
    long_description = 'a' * 1001
    with pytest.raises(ValueError, match='Description must be 1000 characters or less'):
        TodoDescription(long_description)


def test_str_representation():
    """Test the string representation of TodoDescription."""
    description = TodoDescription('Test description')
    assert str(description) == 'Test description'
