# Changelog

All notable changes to Terminal Window Management (TWM) will be documented in this file.

## [0.1.0] - 2026-01-31

### Added
- Initial release of TWM
- Window positioning commands (left, right, quadrant, center, maximize)
- Grid layout support for arranging multiple windows
- Color management system with theme and tab color support
- Profile system for saving and loading window layouts
- Window grouping for organizing related windows
- Multi-display support with automatic screen detection
- CLI interface built with Click
- AppleScript integration via PyObjC for Terminal.app control
- Configuration storage in `~/.config/twm/`
- Comprehensive documentation and examples
- Example profiles for common workflows (dev-env, code-review, monitoring)
- Basic test suite

### Features
- **Window Positioning**: Tile windows to halves, quadrants, or custom positions
- **Grid Layouts**: Arrange windows in any grid pattern (2x2, 3x2, etc.)
- **Color Support**: Apply Terminal.app themes and custom colors
- **Profiles**: Save complete window layouts with positions, commands, and colors
- **Groups**: Organize windows into named groups
- **Multi-Display**: Automatically detects and works across multiple monitors

### Commands
- `twm left/right` - Tile to screen halves
- `twm quadrant` - Tile to screen quadrants
- `twm center` - Center window with optional size
- `twm maximize` - Maximize window
- `twm grid` - Arrange in grid pattern
- `twm position` - Custom positioning
- `twm list` - List all windows
- `twm screens` - Show screen info
- `twm color theme/tab/bg/fg` - Color management
- `twm profile save/load/list/delete/edit` - Profile management
- `twm group create/add/remove/activate/list/delete` - Group management

### Technical
- Python 3.9+ support
- PyObjC for native macOS integration
- Pydantic for data validation
- YAML for human-readable configuration
- Click for CLI framework

## [Unreleased]

### Planned Features
- Shell completion scripts (bash, zsh, fish)
- Percentage-based positioning (e.g., "50%x50%")
- Profile templates and presets
- Automatic window detection and tracking
- Integration with other terminal emulators (iTerm2, Alacritty)
- GUI for visual profile editing
- Keyboard shortcuts integration
- Window animation support
- Custom color schemes management
