# TWM Quick Start Guide

Get started with Terminal Window Management in 5 minutes!

## Installation

```bash
cd terminal-window-management
pip install -e .
```

## Your First Commands

### 1. List Windows

```bash
twm list
```

This shows all your Terminal windows with their IDs and positions.

### 2. Split Screen

```bash
# Open two Terminal windows, then:
twm left 1    # Move window 1 to left half
twm right 2   # Move window 2 to right half
```

Or just use the frontmost window:

```bash
twm left      # Move current window to left
```

### 3. Grid Layout

```bash
# Open 4 Terminal windows, then:
twm grid 2x2
```

Your windows will be arranged in a 2×2 grid automatically!

### 4. Add Colors

```bash
# Color-code your windows
twm color tab blue 1
twm color tab green 2
twm color tab red 3
twm color tab yellow 4
```

### 5. Save Your Layout

```bash
# Save the current layout as a profile
twm profile save my-workspace
```

### 6. Restore Layout Later

```bash
# Restore your saved layout
twm profile load my-workspace
```

## Common Workflows

### Side-by-Side Coding

```bash
# Window 1: Left half (your code)
twm left 1

# Window 2: Right half (tests/docs)
twm right 2

# Color code them
twm color tab blue 1
twm color tab green 2

# Save it
twm profile save coding
```

### Quadrant Layout

```bash
# 4 windows, one in each corner
twm quadrant ul 1  # Upper-left
twm quadrant ur 2  # Upper-right
twm quadrant dl 3  # Down-left
twm quadrant dr 4  # Down-right
```

### Apply Themes

```bash
# See available themes
twm color list-themes

# Apply a theme
twm color theme Pro 1
twm color theme Ocean 2
```

## Next Steps

- Read the full [README.md](README.md) for all features
- Check out example profiles in `twm/examples/`
- Create custom profiles by editing YAML files in `~/.config/twm/profiles/`

## Tips

- Window IDs are shown with `twm list`
- If you don't specify a window ID, TWM uses the frontmost window
- Profiles can include window positions, colors, themes, and startup commands
- Groups let you organize related windows together

## Need Help?

```bash
twm --help              # General help
twm color --help        # Color commands help
twm profile --help      # Profile commands help
twm group --help        # Group commands help
```

Happy window managing!
