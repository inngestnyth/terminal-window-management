"""Terminal.app control via AppleScript using PyObjC."""

from typing import List, Dict, Tuple, Optional
import AppKit
from Foundation import NSAppleScript


class TerminalWindow:
    """Represents a Terminal.app window."""

    def __init__(self, window_id: int, bounds: Tuple[int, int, int, int], title: str = ""):
        self.window_id = window_id
        self.x, self.y, self.width, self.height = bounds
        self.title = title

    def __repr__(self):
        return f"TerminalWindow(id={self.window_id}, bounds=({self.x}, {self.y}, {self.width}, {self.height}), title='{self.title}')"


def execute_applescript(script: str) -> Optional[str]:
    """Execute an AppleScript and return the result."""
    applescript = NSAppleScript.alloc().initWithSource_(script)
    result, error = applescript.executeAndReturnError_(None)

    if error:
        raise RuntimeError(f"AppleScript error: {error}")

    if result:
        return result.stringValue()
    return None


def get_windows() -> List[TerminalWindow]:
    """Get all Terminal.app windows with their properties."""
    script = """
    tell application "System Events"
        tell process "Terminal"
            set windowList to ""
            repeat with w from 1 to count of windows
                try
                    set windowPos to position of window w
                    set windowSize to size of window w
                    set windowTitle to name of window w
                    set windowList to windowList & w & "|" & (item 1 of windowPos) & "|" & (item 2 of windowPos) & "|" & (item 1 of windowSize) & "|" & (item 2 of windowSize) & "|" & windowTitle & "|||"
                end try
            end repeat
            return windowList
        end tell
    end tell
    """

    result = execute_applescript(script)
    if not result:
        return []

    # Parse the result - windows separated by |||, fields by |
    windows = []
    window_strings = result.split('|||')

    for window_str in window_strings:
        if not window_str.strip():
            continue

        try:
            parts = window_str.split('|')
            if len(parts) < 5:
                continue

            window_id = int(parts[0])
            x = int(float(parts[1]))
            y = int(float(parts[2]))
            width = int(float(parts[3]))
            height = int(float(parts[4]))
            title = parts[5] if len(parts) > 5 else ""

            windows.append(TerminalWindow(window_id, (x, y, width, height), title))
        except (ValueError, IndexError):
            continue

    return windows


def get_frontmost_window() -> Optional[TerminalWindow]:
    """Get the frontmost Terminal.app window."""
    windows = get_windows()
    return windows[0] if windows else None


def set_window_bounds(window_id: int, x: int, y: int, width: int, height: int) -> None:
    """Set the position and size of a Terminal window."""
    script = f"""
    tell application "System Events"
        tell process "Terminal"
            set position of window {window_id} to {{{x}, {y}}}
            set size of window {window_id} to {{{width}, {height}}}
        end tell
    end tell
    """
    execute_applescript(script)


def create_window(profile: Optional[str] = None, command: Optional[str] = None,
                  working_dir: Optional[str] = None) -> None:
    """Create a new Terminal window with optional profile and command."""
    script_parts = ['tell application "Terminal"', 'activate']

    if profile:
        script_parts.append(f'set newWindow to do script "" with profile "{profile}"')
    else:
        script_parts.append('set newWindow to do script ""')

    if working_dir:
        script_parts.append(f'do script "cd {working_dir}" in newWindow')

    if command:
        script_parts.append(f'do script "{command}" in newWindow')

    script_parts.append('end tell')

    script = '\n'.join(script_parts)
    execute_applescript(script)


def get_screen_dimensions() -> Tuple[int, int]:
    """Get the dimensions of the main screen."""
    screen = AppKit.NSScreen.mainScreen()
    frame = screen.frame()
    return int(frame.size.width), int(frame.size.height)


def get_all_screens() -> List[Dict[str, int]]:
    """Get dimensions and positions of all screens."""
    screens = []
    for screen in AppKit.NSScreen.screens():
        frame = screen.frame()
        screens.append({
            'x': int(frame.origin.x),
            'y': int(frame.origin.y),
            'width': int(frame.size.width),
            'height': int(frame.size.height)
        })
    return screens


def set_window_profile(window_id: int, profile_name: str) -> None:
    """Apply a Terminal.app profile to a window."""
    script = f"""
    tell application "Terminal"
        set current settings of window {window_id} to settings set "{profile_name}"
    end tell
    """
    execute_applescript(script)


def set_tab_color(window_id: int, tab_index: int, color: Tuple[int, int, int]) -> None:
    """Set the color of a tab in a Terminal window.

    Args:
        window_id: The window ID
        tab_index: The tab index (1-based)
        color: RGB tuple with values 0-65535
    """
    r, g, b = color
    script = f"""
    tell application "Terminal"
        set tab color of tab {tab_index} of window {window_id} to {{{r}, {g}, {b}}}
    end tell
    """
    execute_applescript(script)


def set_window_colors(window_id: int, bg_color: Optional[Tuple[int, int, int]] = None,
                      fg_color: Optional[Tuple[int, int, int]] = None) -> None:
    """Set custom background and foreground colors for a Terminal window.

    Args:
        window_id: The window ID
        bg_color: Background RGB tuple with values 0-65535
        fg_color: Foreground RGB tuple with values 0-65535
    """
    script_parts = ['tell application "Terminal"']

    if bg_color:
        r, g, b = bg_color
        script_parts.append(f'set background color of window {window_id} to {{{r}, {g}, {b}}}')

    if fg_color:
        r, g, b = fg_color
        script_parts.append(f'set normal text color of window {window_id} to {{{r}, {g}, {b}}}')

    script_parts.append('end tell')

    script = '\n'.join(script_parts)
    execute_applescript(script)


def get_available_profiles() -> List[str]:
    """Get list of available Terminal.app profiles."""
    script = """
    tell application "Terminal"
        return name of every settings set
    end tell
    """
    result = execute_applescript(script)
    if not result:
        return []

    # Parse comma-separated list
    return [profile.strip() for profile in result.split(',')]


def bring_window_to_front(window_id: int) -> None:
    """Bring a Terminal window to the front."""
    script = f"""
    tell application "System Events"
        tell process "Terminal"
            set frontmost to true
            perform action "AXRaise" of window {window_id}
        end tell
    end tell
    """
    execute_applescript(script)


def close_window(window_id: int) -> None:
    """Close a Terminal window."""
    script = f"""
    tell application "Terminal"
        close window {window_id}
    end tell
    """
    execute_applescript(script)
