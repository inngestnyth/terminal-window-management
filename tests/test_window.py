"""Tests for window positioning logic."""

import pytest
from twm import terminal


def test_terminal_window_creation():
    """Test TerminalWindow object creation."""
    window = terminal.TerminalWindow(1, (0, 23, 1920, 1080), "Terminal")
    assert window.window_id == 1
    assert window.x == 0
    assert window.y == 23
    assert window.width == 1920
    assert window.height == 1080
    assert window.title == "Terminal"


def test_terminal_window_repr():
    """Test TerminalWindow string representation."""
    window = terminal.TerminalWindow(1, (0, 23, 1920, 1080), "Test")
    repr_str = repr(window)
    assert 'TerminalWindow' in repr_str
    assert 'id=1' in repr_str
    assert 'Test' in repr_str
