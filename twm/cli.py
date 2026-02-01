"""Command-line interface for Terminal Window Management."""

import click
from typing import Optional
from . import terminal, window, colors, profiles, groups


@click.group()
@click.version_option(version='0.1.0')
def main():
    """Terminal Window Management (TWM) - Manage macOS Terminal.app windows."""
    pass


# Window positioning commands
@main.command()
@click.argument('window_id', type=int, required=False)
def left(window_id: Optional[int]):
    """Move window to left half of screen."""
    try:
        window.tile_left(window_id)
        click.echo("Window moved to left half")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument('window_id', type=int, required=False)
def right(window_id: Optional[int]):
    """Move window to right half of screen."""
    try:
        window.tile_right(window_id)
        click.echo("Window moved to right half")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument('quadrant', type=click.Choice(['ul', 'ur', 'dl', 'dr'], case_sensitive=False))
@click.argument('window_id', type=int, required=False)
def quadrant(quadrant: str, window_id: Optional[int]):
    """Move window to a quadrant.

    QUADRANT: ul (upper-left), ur (upper-right), dl (down-left), dr (down-right)
    """
    try:
        window.tile_quadrant(window_id, quadrant)
        click.echo(f"Window moved to {quadrant} quadrant")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument('window_id', type=int, required=False)
@click.option('--width', type=int, help='Window width in pixels')
@click.option('--height', type=int, help='Window height in pixels')
def center(window_id: Optional[int], width: Optional[int], height: Optional[int]):
    """Center window on screen with optional custom size."""
    try:
        window.center(window_id, width, height)
        click.echo("Window centered")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument('window_id', type=int, required=False)
def maximize(window_id: Optional[int]):
    """Maximize window to fill screen."""
    try:
        window.maximize(window_id)
        click.echo("Window maximized")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument('layout', type=str)
@click.argument('window_ids', type=int, nargs=-1)
def grid(layout: str, window_ids: tuple):
    """Arrange windows in a grid layout.

    LAYOUT: Format like "2x2" for 2 rows and 2 columns
    WINDOW_IDS: Optional list of window IDs to arrange (uses all if not specified)
    """
    try:
        # Parse layout string like "2x2"
        if 'x' not in layout.lower():
            raise ValueError("Layout must be in format like '2x2' (rows x columns)")

        rows, cols = map(int, layout.lower().split('x'))
        window_list = list(window_ids) if window_ids else None

        window.tile_grid(rows, cols, window_list)
        click.echo(f"Windows arranged in {rows}x{cols} grid")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument('window_id', type=int, required=False)
@click.option('-x', '--x-pos', type=int, required=True, help='X position')
@click.option('-y', '--y-pos', type=int, required=True, help='Y position')
@click.option('-w', '--width', type=int, required=True, help='Width')
@click.option('-h', '--height', type=int, required=True, help='Height')
def position(window_id: Optional[int], x_pos: int, y_pos: int, width: int, height: int):
    """Set exact window position and size."""
    try:
        window.custom_position(window_id, x_pos, y_pos, width, height)
        click.echo(f"Window positioned at ({x_pos}, {y_pos}) with size {width}x{height}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command()
def list():
    """List all Terminal windows."""
    try:
        windows = terminal.get_windows()
        if not windows:
            click.echo("No Terminal windows found")
            return

        click.echo(f"Found {len(windows)} window(s):\n")
        for w in windows:
            click.echo(f"  Window {w.window_id}: {w.title}")
            click.echo(f"    Position: ({w.x}, {w.y})")
            click.echo(f"    Size: {w.width}x{w.height}")
            click.echo()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@main.command()
def screens():
    """Show screen dimensions."""
    try:
        screen_list = terminal.get_all_screens()
        if not screen_list:
            click.echo("No screens found")
            return

        click.echo(f"Found {len(screen_list)} screen(s):\n")
        for idx, screen in enumerate(screen_list, 1):
            click.echo(f"  Screen {idx}:")
            click.echo(f"    Position: ({screen['x']}, {screen['y']})")
            click.echo(f"    Size: {screen['width']}x{screen['height']}")
            click.echo()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


# Color commands group
@main.group()
def color():
    """Color and theme management commands."""
    pass


@color.command(name='theme')
@click.argument('profile_name', type=str)
@click.argument('window_id', type=int, required=False)
def color_theme(profile_name: str, window_id: Optional[int]):
    """Apply Terminal.app theme/profile to window."""
    try:
        wid = window.get_target_window_id(window_id)
        colors.apply_profile(wid, profile_name)
        click.echo(f"Applied theme '{profile_name}' to window {wid}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@color.command(name='tab')
@click.argument('color_name', type=str)
@click.argument('window_id', type=int, required=False)
@click.option('--tab-index', type=int, default=1, help='Tab index (default: 1)')
def color_tab(color_name: str, window_id: Optional[int], tab_index: int):
    """Set tab color."""
    try:
        wid = window.get_target_window_id(window_id)
        colors.set_tab_color_by_name(wid, tab_index, color_name)
        click.echo(f"Set tab {tab_index} color to '{color_name}' in window {wid}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@color.command(name='bg')
@click.argument('color_value', type=str)
@click.argument('window_id', type=int, required=False)
def color_bg(color_value: str, window_id: Optional[int]):
    """Set background color."""
    try:
        wid = window.get_target_window_id(window_id)
        colors.set_background_color(wid, color_value)
        click.echo(f"Set background color to '{color_value}' in window {wid}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@color.command(name='fg')
@click.argument('color_value', type=str)
@click.argument('window_id', type=int, required=False)
def color_fg(color_value: str, window_id: Optional[int]):
    """Set foreground/text color."""
    try:
        wid = window.get_target_window_id(window_id)
        colors.set_foreground_color(wid, color_value)
        click.echo(f"Set text color to '{color_value}' in window {wid}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@color.command(name='list-themes')
def color_list_themes():
    """List available Terminal.app themes."""
    try:
        themes = terminal.get_available_profiles()
        if not themes:
            click.echo("No themes found")
            return

        click.echo(f"Available themes ({len(themes)}):\n")
        for theme in themes:
            click.echo(f"  - {theme}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@color.command(name='reset')
@click.argument('window_id', type=int, required=False)
def color_reset(window_id: Optional[int]):
    """Reset to default Terminal.app colors."""
    try:
        wid = window.get_target_window_id(window_id)
        colors.apply_profile(wid, 'Basic')
        click.echo(f"Reset colors to default in window {wid}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


# Profile commands group
@main.group()
def profile():
    """Profile management commands."""
    pass


@profile.command(name='save')
@click.argument('name', type=str)
@click.option('--description', '-d', type=str, default='', help='Profile description')
def profile_save(name: str, description: str):
    """Save current window layout as a profile."""
    try:
        profiles.save_profile(name, description)
        click.echo(f"Profile '{name}' saved successfully")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@profile.command(name='load')
@click.argument('name', type=str)
def profile_load(name: str):
    """Load and apply a saved profile."""
    try:
        profiles.load_profile(name)
        click.echo(f"Profile '{name}' loaded successfully")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@profile.command(name='list')
def profile_list():
    """List all saved profiles."""
    try:
        profile_list = profiles.list_profiles()
        if not profile_list:
            click.echo("No profiles found")
            return

        click.echo(f"Saved profiles ({len(profile_list)}):\n")
        for prof in profile_list:
            click.echo(f"  - {prof['name']}")
            if prof.get('description'):
                click.echo(f"    {prof['description']}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@profile.command(name='delete')
@click.argument('name', type=str)
@click.confirmation_option(prompt='Are you sure you want to delete this profile?')
def profile_delete(name: str):
    """Delete a saved profile."""
    try:
        profiles.delete_profile(name)
        click.echo(f"Profile '{name}' deleted successfully")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@profile.command(name='edit')
@click.argument('name', type=str)
def profile_edit(name: str):
    """Edit a profile in $EDITOR."""
    try:
        profiles.edit_profile(name)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


# Group commands
@main.group()
def group():
    """Window grouping commands."""
    pass


@group.command(name='create')
@click.argument('name', type=str)
@click.argument('window_ids', type=int, nargs=-1)
def group_create(name: str, window_ids: tuple):
    """Create a window group."""
    try:
        groups.create_group(name, list(window_ids))
        click.echo(f"Group '{name}' created with {len(window_ids)} window(s)")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@group.command(name='add')
@click.argument('name', type=str)
@click.argument('window_id', type=int)
def group_add(name: str, window_id: int):
    """Add a window to an existing group."""
    try:
        groups.add_to_group(name, window_id)
        click.echo(f"Added window {window_id} to group '{name}'")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@group.command(name='remove')
@click.argument('name', type=str)
@click.argument('window_id', type=int)
def group_remove(name: str, window_id: int):
    """Remove a window from a group."""
    try:
        groups.remove_from_group(name, window_id)
        click.echo(f"Removed window {window_id} from group '{name}'")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@group.command(name='activate')
@click.argument('name', type=str)
def group_activate(name: str):
    """Bring a group to the front."""
    try:
        groups.activate_group(name)
        click.echo(f"Activated group '{name}'")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@group.command(name='list')
def group_list():
    """List all window groups."""
    try:
        group_list = groups.list_groups()
        if not group_list:
            click.echo("No groups found")
            return

        click.echo(f"Window groups ({len(group_list)}):\n")
        for grp in group_list:
            click.echo(f"  - {grp['name']}: {len(grp['windows'])} window(s)")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@group.command(name='delete')
@click.argument('name', type=str)
@click.confirmation_option(prompt='Are you sure you want to delete this group?')
def group_delete(name: str):
    """Delete a window group."""
    try:
        groups.delete_group(name)
        click.echo(f"Group '{name}' deleted successfully")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    main()
