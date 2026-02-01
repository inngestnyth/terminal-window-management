# TWM Project Structure

```
terminal-window-management/
├── twm/                        # Main package
│   ├── __init__.py            # Package initialization
│   ├── cli.py                 # CLI interface (Click)
│   ├── terminal.py            # Terminal.app control (AppleScript/PyObjC)
│   ├── window.py              # Window positioning logic
│   ├── colors.py              # Color and theme management
│   ├── profiles.py            # Profile save/load functionality
│   ├── groups.py              # Window grouping
│   ├── config.py              # Configuration handling
│   └── examples/              # Example profiles
│       ├── dev-env.yaml       # 3-window dev setup
│       ├── code-review.yaml   # Side-by-side review
│       └── monitoring.yaml    # 4-window monitoring grid
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_colors.py         # Color parsing tests
│   ├── test_window.py         # Window logic tests
│   └── test_profiles.py       # Profile management tests
│
├── setup.py                    # Package setup and entry points
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore patterns
│
├── README.md                   # Main documentation
├── QUICKSTART.md              # Quick start guide
├── CHANGELOG.md               # Version history
├── PROJECT_STRUCTURE.md       # This file
└── LICENSE                     # MIT License
```

## Runtime Configuration

When TWM runs, it creates configuration directories:

```
~/.config/twm/
├── profiles/                   # User-saved profiles
│   ├── my-workspace.yaml
│   ├── dev-env.yaml
│   └── ...
├── groups.yaml                 # Window groups
└── config.yaml                 # Main config (future use)
```

## Module Responsibilities

### Core Modules

**terminal.py**
- AppleScript execution via PyObjC
- Terminal.app window detection and control
- Screen dimension detection
- Window manipulation (position, size, colors, themes)

**window.py**
- High-level positioning operations (left, right, quadrants)
- Grid layout calculations
- Multi-display screen detection
- Position validation and adjustment

**colors.py**
- Color parsing (hex, RGB, named colors)
- Terminal.app theme/profile application
- Tab color management
- Custom foreground/background colors

**profiles.py**
- Profile serialization/deserialization (YAML)
- Window layout capture and restoration
- Profile CRUD operations
- Editor integration for manual editing

**groups.py**
- Window group management
- Group persistence
- Window activation and focus management

**config.py**
- Configuration directory management
- Path utilities for profiles and groups

**cli.py**
- Click-based command-line interface
- Command routing and validation
- User-facing error handling
- Help text and documentation

## Data Models

### TerminalWindow
```python
TerminalWindow(
    window_id: int,
    bounds: (x, y, width, height),
    title: str
)
```

### Profile
```python
Profile(
    name: str,
    description: str,
    windows: List[WindowConfig]
)
```

### WindowConfig
```python
WindowConfig(
    position: {x, y, width, height},
    title: str,
    working_dir: str,
    command: str,
    theme: str,
    tab_color: str,
    background_color: str,
    text_color: str
)
```

### WindowGroup
```python
WindowGroup(
    name: str,
    windows: List[int],
    layout: str
)
```

## Entry Points

The CLI is accessible via:

```bash
twm <command> [options]
```

Entry point defined in `setup.py`:
```python
entry_points={
    'console_scripts': [
        'twm=twm.cli:main',
    ],
}
```

## Dependencies

- **Click** (≥8.0.0): CLI framework
- **PyObjC** (≥9.0): macOS/AppleScript integration
- **PyYAML** (≥6.0): Configuration file handling
- **Pydantic** (≥2.0): Data validation and serialization

## Testing

Run tests with:
```bash
pytest tests/
```

Test coverage includes:
- Color parsing and conversion
- Window object creation
- Profile serialization
- Data model validation
