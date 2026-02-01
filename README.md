# Terminal Window Management (TWM)

A modern Python CLI tool for managing macOS Terminal.app windows with support for positioning, sizing, grouping, and profiles.

**🚀 [Quick Start Guide](GETTING_STARTED.md)** | [Installation](INSTALL.md) | [Full Documentation](#)

## Features

- **Window Positioning**: Tile windows to left/right halves, quadrants, or custom positions
- **Grid Layouts**: Arrange multiple windows in grid patterns (2x2, 3x2, etc.)
- **Color Management**: Apply Terminal.app themes and custom colors to windows and tabs
- **Profiles**: Save and restore complete window layouts with positions, commands, and colors
- **Grouping**: Organize windows into named groups for easy management
- **Multi-Display Support**: Automatically detects and works with multiple monitors

## Installation

### Requirements

- macOS 10.14 or later
- Python 3.9 or later
- Terminal.app

### Install from source

```bash
# Navigate to the project directory
cd "Terminal Window Management"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install TWM
pip install -e .
```

**Important:** After installation, you need to grant Python accessibility permissions. See [GETTING_STARTED.md](GETTING_STARTED.md) for details.

### Verify installation

```bash
twm --version
# Output: twm, version 0.1.0
```

## Quick Start

```bash
# List all terminal windows
twm list

# Move frontmost window to left half of screen
twm left

# Move frontmost window to right half
twm right

# Move specific window (by ID) to upper-left quadrant
twm quadrant ul 1

# Arrange all windows in a 2x2 grid
twm grid 2x2

# Center window with custom size
twm center --width 1200 --height 800

# Maximize window
twm maximize
```

## Window Positioning Commands

### Basic Tiling

```bash
# Tile to left half
twm left [WINDOW_ID]

# Tile to right half
twm right [WINDOW_ID]

# Tile to quadrant (ul, ur, dl, dr)
twm quadrant ul [WINDOW_ID]
twm quadrant ur [WINDOW_ID]
twm quadrant dl [WINDOW_ID]
twm quadrant dr [WINDOW_ID]
```

### Advanced Positioning

```bash
# Center window
twm center [WINDOW_ID]

# Center with custom size
twm center --width 1200 --height 800

# Maximize window
twm maximize [WINDOW_ID]

# Custom position and size
twm position -x 0 -y 23 -w 1920 -h 1080 [WINDOW_ID]

# Arrange windows in grid
twm grid 2x2              # All windows in 2x2 grid
twm grid 3x2 1 2 3 4 5 6  # Specific windows in 3x2 grid
```

### Utility Commands

```bash
# List all windows with IDs and positions
twm list

# Show screen dimensions
twm screens
```

## Color and Theme Management

### Apply Themes

```bash
# List available Terminal.app themes
twm color list-themes

# Apply a theme to frontmost window
twm color theme Pro

# Apply theme to specific window
twm color theme Ocean 1
```

### Tab Colors

```bash
# Set tab color using preset names
twm color tab red
twm color tab blue 1      # For specific window

# Set tab color using hex
twm color tab "#FF5733"

# Available preset colors:
# red, green, blue, yellow, purple, orange, cyan, magenta,
# white, black, gray, darkgray, lightgray
```

### Custom Colors

```bash
# Set background color
twm color bg "#1a1a1a"

# Set foreground/text color
twm color fg "#00ff00"

# Reset to default colors
twm color reset
```

### Color Format Support

TWM supports multiple color formats:

- **Named colors**: `red`, `green`, `blue`, `yellow`, `purple`, `orange`, etc.
- **Hex colors**: `#FF5733` or `FF5733`
- **RGB format**: `rgb(255, 87, 51)`

## Profile Management

Profiles allow you to save and restore complete window layouts, including positions, colors, themes, and startup commands.

### Basic Profile Usage

```bash
# Save current window layout
twm profile save mysetup

# Save with description
twm profile save dev-env --description "Development environment setup"

# Load a profile
twm profile load mysetup

# List all profiles
twm profile list

# Delete a profile
twm profile delete mysetup

# Edit profile YAML manually
twm profile edit mysetup
```

### Profile Format

Profiles are stored as YAML files in `~/.config/twm/profiles/`. Here's an example:

```yaml
name: "development"
description: "3-window dev setup"
windows:
  - position:
      x: 0
      y: 23
      width: 960
      height: 1080
    title: "editor"
    working_dir: "~/projects/myapp"
    theme: "Pro"
    tab_color: "blue"

  - position:
      x: 960
      y: 23
      width: 960
      height: 540
    title: "server"
    working_dir: "~/projects/myapp"
    command: "npm run dev"
    theme: "Ocean"
    tab_color: "green"

  - position:
      x: 960
      y: 563
      width: 960
      height: 540
    title: "logs"
    working_dir: "~/projects/myapp"
    command: "tail -f logs/app.log"
    background_color: "#1a1a1a"
    text_color: "#00ff00"
    tab_color: "red"
```

## Window Grouping

Groups let you organize and manage related windows together.

```bash
# Create a group with specific windows
twm group create dev 1 2 3

# Add window to existing group
twm group add dev 4

# Remove window from group
twm group remove dev 4

# Bring all windows in group to front
twm group activate dev

# List all groups
twm group list

# Delete a group
twm group delete dev
```

## Common Workflows

### Development Setup

```bash
# Create 3 windows for development
# Window 1: Code editor (left half)
twm left 1

# Window 2: Server logs (top-right quadrant)
twm quadrant ur 2

# Window 3: Terminal (bottom-right quadrant)
twm quadrant dr 3

# Apply colors to distinguish windows
twm color tab blue 1
twm color tab green 2
twm color tab red 3

# Save as profile
twm profile save dev-env --description "Development environment"
```

### Code Review Setup

```bash
# Create 2-window side-by-side layout
twm grid 1x2

# Apply different themes
twm color theme Pro 1
twm color theme Ocean 2

# Save as profile
twm profile save code-review
```

### Multi-Monitor Workflow

```bash
# Check screen dimensions
twm screens

# TWM automatically detects which screen each window is on
# and tiles accordingly
twm left     # Tiles on current window's screen
twm right    # Works across all monitors
```

## Configuration

Configuration files are stored in `~/.config/twm/`:

```
~/.config/twm/
├── profiles/           # Saved window layouts
│   ├── dev-env.yaml
│   └── code-review.yaml
├── groups.yaml         # Window groups
└── config.yaml         # Main configuration (future use)
```

## Examples

### Example 1: Basic Window Management

```bash
# Open 4 terminal windows, then:
twm grid 2x2
twm color tab red 1
twm color tab green 2
twm color tab blue 3
twm color tab yellow 4
```

### Example 2: Save Current Layout

```bash
# Arrange windows as you like, then:
twm profile save my-layout --description "My preferred workspace"

# Later, restore it:
twm profile load my-layout
```

### Example 3: Create a Group

```bash
# Create a group for project windows
twm group create project 1 2 3

# When you need to focus on the project:
twm group activate project
```

## Tips and Tricks

1. **Window IDs**: When no window ID is specified, TWM uses the frontmost window
2. **Multi-Display**: TWM automatically detects which screen a window is on
3. **Menu Bar**: TWM accounts for macOS menu bar height (23px) automatically
4. **Profiles**: Edit profile YAML files manually for fine-grained control
5. **Themes**: Use `twm color list-themes` to see all available Terminal.app themes

## Troubleshooting

### "No Terminal windows found"

Make sure Terminal.app is running with at least one window open.

### AppleScript Permissions

On first run, macOS may ask for permission to control Terminal.app. Grant this permission in System Preferences > Security & Privacy > Privacy > Automation.

### Window Positioning Issues

If windows aren't positioning correctly:
- Check screen dimensions with `twm screens`
- Verify window IDs with `twm list`
- Try maximizing first: `twm maximize`

## Development

### Running Tests

```bash
pytest tests/
```

### Project Structure

```
twm/
├── __init__.py       # Package initialization
├── cli.py            # CLI interface (Click)
├── terminal.py       # Terminal.app control (AppleScript)
├── window.py         # Window positioning logic
├── colors.py         # Color/theme management
├── profiles.py       # Profile save/load
├── groups.py         # Window grouping
└── config.py         # Configuration handling
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

Inspired by [termtile](https://github.com/apaszke/termtile) but modernized with Python, profiles, grouping, and color management.

## Related Projects

- [termtile](https://github.com/apaszke/termtile) - Original AppleScript-based terminal tiler
- [Rectangle](https://rectangleapp.com/) - General window management for macOS
- [iTerm2](https://iterm2.com/) - Advanced terminal with built-in window management
