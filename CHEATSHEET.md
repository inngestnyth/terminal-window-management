# TWM Command Cheat Sheet

Quick reference for Terminal Window Management commands.

## Setup

```bash
source venv/bin/activate  # Activate TWM environment
```

## Window Positioning

```bash
twm left                   # Move to left half
twm right                  # Move to right half
twm center                 # Center window
twm maximize              # Maximize window

twm quadrant ul           # Upper-left quarter
twm quadrant ur           # Upper-right quarter
twm quadrant dl           # Down-left quarter
twm quadrant dr           # Down-right quarter

twm grid 2x2              # 2x2 grid layout
twm grid 3x2              # 3x2 grid layout

twm position -x 0 -y 23 -w 1920 -h 1080  # Exact position
```

## Window Info

```bash
twm list                  # List all windows with IDs
twm screens               # Show screen dimensions
```

## Colors & Themes

```bash
# Themes
twm color list-themes     # List available themes
twm color theme Pro       # Apply Pro theme
twm color theme Ocean     # Apply Ocean theme
twm color reset           # Reset to default

# Tab Colors
twm color tab red         # Red tab
twm color tab blue        # Blue tab
twm color tab "#FF5733"   # Hex color

# Custom Colors
twm color bg "#1a1a1a"    # Set background
twm color fg "#00ff00"    # Set text color
```

### Available Tab Colors
`red`, `green`, `blue`, `yellow`, `purple`, `orange`, `cyan`, `magenta`, `white`, `black`, `gray`

## Profiles

```bash
# Save & Load
twm profile save dev-env              # Save current layout
twm profile save dev-env -d "My dev"  # With description
twm profile load dev-env              # Restore layout

# Manage
twm profile list          # List all profiles
twm profile edit dev-env  # Edit in $EDITOR
twm profile delete dev-env # Delete profile
```

## Groups

```bash
# Create & Manage
twm group create work 1 2 3    # Create group with windows
twm group add work 4           # Add window to group
twm group remove work 4        # Remove from group

# Use
twm group activate work        # Bring group to front
twm group list                # List all groups
twm group delete work         # Delete group
```

## Common Workflows

### Side-by-Side Coding
```bash
twm left 1                    # Code on left
twm right 2                   # Docs on right
twm color tab blue 1          # Blue tab for code
twm color tab green 2         # Green tab for docs
twm profile save coding       # Save layout
```

### 4-Window Dev Setup
```bash
twm grid 2x2                  # Arrange in grid
twm color tab blue 1          # Editor
twm color tab green 2         # Server
twm color tab red 3           # Logs
twm color tab yellow 4        # Terminal
twm profile save dev-env      # Save layout
```

### Quick Tiling
```bash
# Split screen left/right
twm left && twm right 2

# Or quadrant layout
twm quadrant ul 1
twm quadrant ur 2
twm quadrant dl 3
twm quadrant dr 4
```

## Tips

- **Window IDs**: Use `twm list` to find window IDs
- **Default Window**: If you don't specify a window ID, TWM uses the frontmost window
- **Profiles**: Profiles are stored in `~/.config/twm/profiles/` as YAML files
- **Editing**: Run `twm profile edit <name>` to manually edit profile YAML
- **Help**: Add `--help` to any command for more info (e.g., `twm color --help`)

## Help Commands

```bash
twm --help                # General help
twm color --help          # Color commands
twm profile --help        # Profile commands
twm group --help          # Group commands
```

## Configuration Files

```
~/.config/twm/
├── profiles/             # Your saved profiles
│   └── *.yaml
└── groups.yaml          # Window groups
```

---

**More Info:**
- [Getting Started](GETTING_STARTED.md)
- [Quick Start Guide](QUICKSTART.md)
- [Full Documentation](README.md)
