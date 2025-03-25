"""Tests for TodoTitle value object."""

import pytest

from dddpy.domain.todo.value_objects.todo_title import TodoTitle


def test_create_valid_title():
    """Test that a valid title can be created."""
    title = TodoTitle('Test Todo')
    assert title.value == 'Test Todo'


def test_empty_title_raises_error():
    """Test that creating a title with empty string raises ValueError."""
    with pytest.raises(ValueError, match='Title is required'):
        TodoTitle('')


def test_title_too_long_raises_error():
    """Test that creating a title longer than 100 characters raises ValueError."""
    long_title = 'a' * 101
    with pytest.raises(ValueError, match='Title must be 100 characters or less'):
        TodoTitle(long_title)


def test_str_representation():
    """Test the string representation of TodoTitle."""
    title = TodoTitle('Test Todo')
    assert str(title) == 'Test Todo'
