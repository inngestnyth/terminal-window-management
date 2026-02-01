"""Window positioning and layout management."""

from typing import List, Optional, Tuple
from . import terminal


def get_target_window_id(window_id: Optional[int] = None) -> int:
    """Get the target window ID, defaulting to frontmost window."""
    if window_id is not None:
        return window_id

    frontmost = terminal.get_frontmost_window()
    if not frontmost:
        raise RuntimeError("No Terminal windows found")

    return frontmost.window_id


def get_screen_for_window(window: terminal.TerminalWindow) -> Tuple[int, int, int, int]:
    """Get the screen dimensions for the screen containing the window.

    Returns: (x, y, width, height) of the screen
    """
    screens = terminal.get_all_screens()

    # Find which screen contains the window center
    window_center_x = window.x + window.width // 2
    window_center_y = window.y + window.height // 2

    for screen in screens:
        if (screen['x'] <= window_center_x < screen['x'] + screen['width'] and
                screen['y'] <= window_center_y < screen['y'] + screen['height']):
            return screen['x'], screen['y'], screen['width'], screen['height']

    # Default to main screen if not found
    width, height = terminal.get_screen_dimensions()
    return 0, 0, width, height


def tile_left(window_id: Optional[int] = None) -> None:
    """Position window on the left half of the screen."""
    wid = get_target_window_id(window_id)
    windows = terminal.get_windows()
    window = next((w for w in windows if w.window_id == wid), None)

    if not window:
        raise RuntimeError(f"Window {wid} not found")

    screen_x, screen_y, screen_width, screen_height = get_screen_for_window(window)

    # Account for macOS menu bar (typically 23-25 pixels)
    menu_bar_height = 23
    usable_y = screen_y + menu_bar_height
    usable_height = screen_height - menu_bar_height

    x = screen_x
    y = usable_y
    width = screen_width // 2
    height = usable_height

    terminal.set_window_bounds(wid, x, y, width, height)


def tile_right(window_id: Optional[int] = None) -> None:
    """Position window on the right half of the screen."""
    wid = get_target_window_id(window_id)
    windows = terminal.get_windows()
    window = next((w for w in windows if w.window_id == wid), None)

    if not window:
        raise RuntimeError(f"Window {wid} not found")

    screen_x, screen_y, screen_width, screen_height = get_screen_for_window(window)

    menu_bar_height = 23
    usable_y = screen_y + menu_bar_height
    usable_height = screen_height - menu_bar_height

    x = screen_x + screen_width // 2
    y = usable_y
    width = screen_width // 2
    height = usable_height

    terminal.set_window_bounds(wid, x, y, width, height)


def tile_quadrant(window_id: Optional[int], quadrant: str) -> None:
    """Position window in a quadrant of the screen.

    Args:
        window_id: Window ID or None for frontmost
        quadrant: One of 'ul', 'ur', 'dl', 'dr' (upper-left, upper-right, down-left, down-right)
    """
    wid = get_target_window_id(window_id)
    windows = terminal.get_windows()
    window = next((w for w in windows if w.window_id == wid), None)

    if not window:
        raise RuntimeError(f"Window {wid} not found")

    screen_x, screen_y, screen_width, screen_height = get_screen_for_window(window)

    menu_bar_height = 23
    usable_y = screen_y + menu_bar_height
    usable_height = screen_height - menu_bar_height

    half_width = screen_width // 2
    half_height = usable_height // 2

    quadrant = quadrant.lower()
    if quadrant == 'ul':  # upper-left
        x, y = screen_x, usable_y
    elif quadrant == 'ur':  # upper-right
        x, y = screen_x + half_width, usable_y
    elif quadrant == 'dl':  # down-left
        x, y = screen_x, usable_y + half_height
    elif quadrant == 'dr':  # down-right
        x, y = screen_x + half_width, usable_y + half_height
    else:
        raise ValueError(f"Invalid quadrant: {quadrant}. Must be one of: ul, ur, dl, dr")

    terminal.set_window_bounds(wid, x, y, half_width, half_height)


def center(window_id: Optional[int] = None, width: Optional[int] = None,
           height: Optional[int] = None) -> None:
    """Center window on screen with optional custom size."""
    wid = get_target_window_id(window_id)
    windows = terminal.get_windows()
    window = next((w for w in windows if w.window_id == wid), None)

    if not window:
        raise RuntimeError(f"Window {wid} not found")

    screen_x, screen_y, screen_width, screen_height = get_screen_for_window(window)

    menu_bar_height = 23
    usable_y = screen_y + menu_bar_height
    usable_height = screen_height - menu_bar_height

    # Use current size if not specified
    if width is None:
        width = window.width
    if height is None:
        height = window.height

    # Ensure window fits on screen
    width = min(width, screen_width)
    height = min(height, usable_height)

    x = screen_x + (screen_width - width) // 2
    y = usable_y + (usable_height - height) // 2

    terminal.set_window_bounds(wid, x, y, width, height)


def maximize(window_id: Optional[int] = None) -> None:
    """Maximize window to fill the screen."""
    wid = get_target_window_id(window_id)
    windows = terminal.get_windows()
    window = next((w for w in windows if w.window_id == wid), None)

    if not window:
        raise RuntimeError(f"Window {wid} not found")

    screen_x, screen_y, screen_width, screen_height = get_screen_for_window(window)

    menu_bar_height = 23
    usable_y = screen_y + menu_bar_height
    usable_height = screen_height - menu_bar_height

    terminal.set_window_bounds(wid, screen_x, usable_y, screen_width, usable_height)


def custom_position(window_id: Optional[int], x: int, y: int,
                    width: int, height: int) -> None:
    """Position window at exact coordinates."""
    wid = get_target_window_id(window_id)
    terminal.set_window_bounds(wid, x, y, width, height)


def tile_grid(rows: int, cols: int, window_ids: Optional[List[int]] = None) -> None:
    """Arrange windows in a grid layout.

    Args:
        rows: Number of rows
        cols: Number of columns
        window_ids: Specific window IDs to arrange, or None to use all windows
    """
    if rows < 1 or cols < 1:
        raise ValueError("Rows and columns must be at least 1")

    windows = terminal.get_windows()
    if not windows:
        raise RuntimeError("No Terminal windows found")

    # Filter windows if specific IDs provided
    if window_ids:
        windows = [w for w in windows if w.window_id in window_ids]

    if not windows:
        raise RuntimeError("No windows to arrange")

    # Use the screen of the first window
    screen_x, screen_y, screen_width, screen_height = get_screen_for_window(windows[0])

    menu_bar_height = 23
    usable_y = screen_y + menu_bar_height
    usable_height = screen_height - menu_bar_height

    cell_width = screen_width // cols
    cell_height = usable_height // rows

    # Arrange windows in grid
    for idx, window in enumerate(windows[:rows * cols]):
        row = idx // cols
        col = idx % cols

        x = screen_x + col * cell_width
        y = usable_y + row * cell_height

        terminal.set_window_bounds(window.window_id, x, y, cell_width, cell_height)
