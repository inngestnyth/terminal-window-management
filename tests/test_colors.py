"""Tests for color parsing and management."""

import pytest
from twm import colors


def test_parse_hex_color():
    """Test parsing hex color codes."""
    # With hash
    r, g, b = colors.parse_color('#FF5733')
    assert r == 255 * 257
    assert g == 87 * 257
    assert b == 51 * 257

    # Without hash
    r, g, b = colors.parse_color('FF5733')
    assert r == 255 * 257
    assert g == 87 * 257
    assert b == 51 * 257


def test_parse_rgb_color():
    """Test parsing RGB format."""
    r, g, b = colors.parse_color('rgb(255, 87, 51)')
    assert r == 255 * 257
    assert g == 87 * 257
    assert b == 51 * 257


def test_parse_named_color():
    """Test parsing named colors."""
    r, g, b = colors.parse_color('red')
    assert (r, g, b) == (65535, 0, 0)

    r, g, b = colors.parse_color('green')
    assert (r, g, b) == (0, 65535, 0)

    r, g, b = colors.parse_color('blue')
    assert (r, g, b) == (0, 0, 65535)


def test_invalid_color():
    """Test error handling for invalid colors."""
    with pytest.raises(ValueError):
        colors.parse_color('not-a-color')

    with pytest.raises(ValueError):
        colors.parse_color('rgb(300, 400, 500)')  # Out of range


def test_preset_colors():
    """Test that all preset colors are valid."""
    for color_name in colors.PRESET_COLORS:
        r, g, b = colors.parse_color(color_name)
        assert 0 <= r <= 65535
        assert 0 <= g <= 65535
        assert 0 <= b <= 65535
