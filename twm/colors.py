"""Color and theme management for Terminal windows."""

from typing import Tuple, Optional
from . import terminal


# Preset color mappings (RGB values in 0-65535 range for AppleScript)
PRESET_COLORS = {
    'red': (65535, 0, 0),
    'green': (0, 65535, 0),
    'blue': (0, 0, 65535),
    'yellow': (65535, 65535, 0),
    'purple': (32768, 0, 32768),
    'orange': (65535, 32768, 0),
    'cyan': (0, 65535, 65535),
    'magenta': (65535, 0, 65535),
    'white': (65535, 65535, 65535),
    'black': (0, 0, 0),
    'gray': (32768, 32768, 32768),
    'darkgray': (16384, 16384, 16384),
    'lightgray': (49152, 49152, 49152),
}


def parse_color(color_str: str) -> Tuple[int, int, int]:
    """Parse color from various formats to AppleScript RGB (0-65535).

    Supported formats:
    - Hex: #FF5733 or FF5733
    - RGB: rgb(255, 87, 51)
    - Named: red, green, blue, etc.

    Returns:
        Tuple of (r, g, b) in 0-65535 range
    """
    color_str = color_str.strip()

    # Check if it's a named color
    if color_str.lower() in PRESET_COLORS:
        return PRESET_COLORS[color_str.lower()]

    # Parse hex color
    if color_str.startswith('#'):
        color_str = color_str[1:]

    if len(color_str) == 6:
        try:
            r = int(color_str[0:2], 16)
            g = int(color_str[2:4], 16)
            b = int(color_str[4:6], 16)
            # Convert from 0-255 to 0-65535
            return (r * 257, g * 257, b * 257)
        except ValueError:
            pass

    # Parse rgb(r, g, b) format
    if color_str.lower().startswith('rgb(') and color_str.endswith(')'):
        try:
            rgb_values = color_str[4:-1].split(',')
            r, g, b = [int(v.strip()) for v in rgb_values]
            # Validate range
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError(f"RGB values must be 0-255")
            # Convert from 0-255 to 0-65535
            return (r * 257, g * 257, b * 257)
        except (ValueError, IndexError):
            pass

    raise ValueError(f"Invalid color format: {color_str}")


def apply_profile(window_id: int, profile_name: str) -> None:
    """Apply a Terminal.app profile/theme to a window.

    Args:
        window_id: The window ID
        profile_name: Name of the Terminal.app profile (e.g., 'Pro', 'Ocean', 'Homebrew')
    """
    available = terminal.get_available_profiles()
    if profile_name not in available:
        raise ValueError(f"Profile '{profile_name}' not found. Available: {', '.join(available)}")

    terminal.set_window_profile(window_id, profile_name)


def set_tab_color_by_name(window_id: int, tab_index: int, color_name: str) -> None:
    """Set tab color using a color name or hex value.

    Args:
        window_id: The window ID
        tab_index: Tab index (1-based)
        color_name: Color name (e.g., 'red') or hex (e.g., '#FF0000')
    """
    color = parse_color(color_name)
    terminal.set_tab_color(window_id, tab_index, color)


def set_background_color(window_id: int, color_value: str) -> None:
    """Set window background color.

    Args:
        window_id: The window ID
        color_value: Color name or hex value
    """
    color = parse_color(color_value)
    terminal.set_window_colors(window_id, bg_color=color)


def set_foreground_color(window_id: int, color_value: str) -> None:
    """Set window foreground/text color.

    Args:
        window_id: The window ID
        color_value: Color name or hex value
    """
    color = parse_color(color_value)
    terminal.set_window_colors(window_id, fg_color=color)


def set_custom_colors(window_id: int, bg_color: Optional[str] = None,
                      fg_color: Optional[str] = None) -> None:
    """Set custom background and foreground colors.

    Args:
        window_id: The window ID
        bg_color: Background color (name or hex)
        fg_color: Foreground color (name or hex)
    """
    bg = parse_color(bg_color) if bg_color else None
    fg = parse_color(fg_color) if fg_color else None
    terminal.set_window_colors(window_id, bg_color=bg, fg_color=fg)


def get_available_themes() -> list:
    """Get list of available Terminal.app themes/profiles."""
    return terminal.get_available_profiles()


def create_custom_profile(name: str, bg_color: str, fg_color: str) -> None:
    """Create a custom Terminal.app profile.

    Note: This creates a profile by duplicating an existing one and modifying colors.

    Args:
        name: Name for the new profile
        bg_color: Background color
        fg_color: Foreground color
    """
    # This is more complex and requires creating a .terminal file
    # For now, we'll use the existing set_custom_colors approach
    raise NotImplementedError("Custom profile creation requires manual .terminal file creation")
