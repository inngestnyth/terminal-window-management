"""Profile management for saving and loading window layouts."""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import yaml
from pydantic import BaseModel, Field
from . import terminal, colors, config


class WindowConfig(BaseModel):
    """Configuration for a single window."""
    position: Dict[str, int] = Field(description="Window position and size")
    title: Optional[str] = None
    working_dir: Optional[str] = None
    command: Optional[str] = None
    theme: Optional[str] = None
    tab_color: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None


class Profile(BaseModel):
    """Window layout profile."""
    name: str
    description: str = ""
    windows: List[WindowConfig]


def save_profile(name: str, description: str = "") -> None:
    """Save current window layout as a profile.

    Args:
        name: Profile name
        description: Optional description
    """
    windows = terminal.get_windows()
    if not windows:
        raise RuntimeError("No Terminal windows to save")

    window_configs = []
    for w in windows:
        window_config = WindowConfig(
            position={
                'x': w.x,
                'y': w.y,
                'width': w.width,
                'height': w.height
            },
            title=w.title or None
        )
        window_configs.append(window_config)

    profile = Profile(
        name=name,
        description=description,
        windows=window_configs
    )

    # Save to YAML file
    profiles_dir = config.get_profiles_dir()
    profile_file = profiles_dir / f"{name}.yaml"

    with open(profile_file, 'w') as f:
        yaml.dump(profile.model_dump(), f, default_flow_style=False, sort_keys=False)


def load_profile(name: str) -> None:
    """Load and apply a saved profile.

    Args:
        name: Profile name
    """
    profiles_dir = config.get_profiles_dir()
    profile_file = profiles_dir / f"{name}.yaml"

    if not profile_file.exists():
        raise FileNotFoundError(f"Profile '{name}' not found")

    with open(profile_file, 'r') as f:
        profile_data = yaml.safe_load(f)

    profile = Profile(**profile_data)

    # Create windows according to profile
    for idx, win_config in enumerate(profile.windows):
        pos = win_config.position

        # Create new window with optional settings
        terminal.create_window(
            profile=win_config.theme,
            command=win_config.command,
            working_dir=win_config.working_dir
        )

        # Get the newly created window (it should be the frontmost)
        import time
        time.sleep(0.5)  # Give Terminal time to create the window

        windows = terminal.get_windows()
        if windows:
            new_window_id = windows[0].window_id

            # Set position and size
            terminal.set_window_bounds(
                new_window_id,
                pos['x'],
                pos['y'],
                pos['width'],
                pos['height']
            )

            # Apply theme if specified
            if win_config.theme:
                try:
                    colors.apply_profile(new_window_id, win_config.theme)
                except Exception:
                    pass  # Ignore theme errors

            # Apply tab color if specified
            if win_config.tab_color:
                try:
                    colors.set_tab_color_by_name(new_window_id, 1, win_config.tab_color)
                except Exception:
                    pass  # Ignore color errors

            # Apply custom colors if specified
            if win_config.background_color or win_config.text_color:
                try:
                    colors.set_custom_colors(
                        new_window_id,
                        bg_color=win_config.background_color,
                        fg_color=win_config.text_color
                    )
                except Exception:
                    pass  # Ignore color errors


def list_profiles() -> List[Dict[str, str]]:
    """List all saved profiles.

    Returns:
        List of dicts with 'name' and 'description' keys
    """
    profiles_dir = config.get_profiles_dir()
    profile_files = profiles_dir.glob('*.yaml')

    profiles = []
    for profile_file in profile_files:
        try:
            with open(profile_file, 'r') as f:
                profile_data = yaml.safe_load(f)
                profiles.append({
                    'name': profile_data.get('name', profile_file.stem),
                    'description': profile_data.get('description', '')
                })
        except Exception:
            continue

    return profiles


def delete_profile(name: str) -> None:
    """Delete a saved profile.

    Args:
        name: Profile name
    """
    profiles_dir = config.get_profiles_dir()
    profile_file = profiles_dir / f"{name}.yaml"

    if not profile_file.exists():
        raise FileNotFoundError(f"Profile '{name}' not found")

    profile_file.unlink()


def edit_profile(name: str) -> None:
    """Edit a profile in $EDITOR.

    Args:
        name: Profile name
    """
    profiles_dir = config.get_profiles_dir()
    profile_file = profiles_dir / f"{name}.yaml"

    if not profile_file.exists():
        raise FileNotFoundError(f"Profile '{name}' not found")

    editor = os.environ.get('EDITOR', 'nano')
    subprocess.run([editor, str(profile_file)])
