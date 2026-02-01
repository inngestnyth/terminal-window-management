"""Window grouping and management."""

from typing import List, Dict, Optional
from pathlib import Path
import yaml
from pydantic import BaseModel
from . import terminal, config


class WindowGroup(BaseModel):
    """Represents a group of windows."""
    name: str
    windows: List[int]
    layout: Optional[str] = None


def get_groups_file() -> Path:
    """Get the groups configuration file."""
    return config.get_config_dir() / 'groups.yaml'


def load_groups() -> Dict[str, WindowGroup]:
    """Load all groups from the config file."""
    groups_file = get_groups_file()

    if not groups_file.exists():
        return {}

    with open(groups_file, 'r') as f:
        data = yaml.safe_load(f) or {}

    groups = {}
    for name, group_data in data.items():
        groups[name] = WindowGroup(**group_data)

    return groups


def save_groups(groups: Dict[str, WindowGroup]) -> None:
    """Save all groups to the config file."""
    groups_file = get_groups_file()

    data = {name: group.model_dump() for name, group in groups.items()}

    with open(groups_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def create_group(name: str, window_ids: List[int]) -> None:
    """Create a new window group.

    Args:
        name: Group name
        window_ids: List of window IDs to include
    """
    groups = load_groups()

    if name in groups:
        raise ValueError(f"Group '{name}' already exists")

    # Validate window IDs
    existing_windows = terminal.get_windows()
    existing_ids = {w.window_id for w in existing_windows}

    invalid_ids = [wid for wid in window_ids if wid not in existing_ids]
    if invalid_ids:
        raise ValueError(f"Invalid window IDs: {invalid_ids}")

    group = WindowGroup(name=name, windows=window_ids)
    groups[name] = group
    save_groups(groups)


def add_to_group(group_name: str, window_id: int) -> None:
    """Add a window to an existing group.

    Args:
        group_name: Group name
        window_id: Window ID to add
    """
    groups = load_groups()

    if group_name not in groups:
        raise ValueError(f"Group '{group_name}' not found")

    # Validate window ID
    existing_windows = terminal.get_windows()
    existing_ids = {w.window_id for w in existing_windows}

    if window_id not in existing_ids:
        raise ValueError(f"Window ID {window_id} not found")

    group = groups[group_name]
    if window_id not in group.windows:
        group.windows.append(window_id)
        save_groups(groups)


def remove_from_group(group_name: str, window_id: int) -> None:
    """Remove a window from a group.

    Args:
        group_name: Group name
        window_id: Window ID to remove
    """
    groups = load_groups()

    if group_name not in groups:
        raise ValueError(f"Group '{group_name}' not found")

    group = groups[group_name]
    if window_id in group.windows:
        group.windows.remove(window_id)
        save_groups(groups)
    else:
        raise ValueError(f"Window ID {window_id} not in group '{group_name}'")


def activate_group(name: str) -> None:
    """Bring all windows in a group to the front.

    Args:
        name: Group name
    """
    groups = load_groups()

    if name not in groups:
        raise ValueError(f"Group '{name}' not found")

    group = groups[name]

    # Get current windows
    existing_windows = terminal.get_windows()
    existing_ids = {w.window_id for w in existing_windows}

    # Filter out window IDs that no longer exist
    valid_window_ids = [wid for wid in group.windows if wid in existing_ids]

    if not valid_window_ids:
        raise RuntimeError(f"No windows in group '{name}' are currently open")

    # Update group if some windows were removed
    if len(valid_window_ids) != len(group.windows):
        group.windows = valid_window_ids
        save_groups(groups)

    # Bring each window to front
    for window_id in reversed(valid_window_ids):
        try:
            terminal.bring_window_to_front(window_id)
        except Exception:
            pass  # Ignore errors for individual windows


def list_groups() -> List[Dict[str, any]]:
    """List all window groups.

    Returns:
        List of dicts with group information
    """
    groups = load_groups()

    result = []
    for name, group in groups.items():
        result.append({
            'name': name,
            'windows': group.windows,
            'layout': group.layout
        })

    return result


def delete_group(name: str) -> None:
    """Delete a window group.

    Args:
        name: Group name
    """
    groups = load_groups()

    if name not in groups:
        raise ValueError(f"Group '{name}' not found")

    del groups[name]
    save_groups(groups)


def get_group(name: str) -> Optional[WindowGroup]:
    """Get a specific group by name.

    Args:
        name: Group name

    Returns:
        WindowGroup or None if not found
    """
    groups = load_groups()
    return groups.get(name)
