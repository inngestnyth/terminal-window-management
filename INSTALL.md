# Installation Guide

This guide will help you install Terminal Window Management (TWM) on macOS.

## Prerequisites

- macOS 10.14 or later
- Python 3.9 or later
- Terminal.app
- Xcode Command Line Tools (for some PyObjC dependencies)

### Install Xcode Command Line Tools

If you haven't already:

```bash
xcode-select --install
```

### Check Python Version

```bash
python3 --version
```

Should show Python 3.9 or later.

## Installation Methods

### Method 1: Using pip (Recommended)

#### Step 1: Create a Virtual Environment

```bash
cd /path/to/terminal-window-management
python3 -m venv venv
source venv/bin/activate
```

#### Step 2: Install TWM

```bash
pip install -e .
```

The `-e` flag installs in "editable" mode, which is useful for development.

#### Step 3: Verify Installation

```bash
twm --version
```

You should see: `twm, version 0.1.0`

### Method 2: Using pipx (Isolated Installation)

If you want TWM available system-wide without a virtual environment:

```bash
# Install pipx if you haven't
brew install pipx

# Install TWM
pipx install /path/to/terminal-window-management
```

### Method 3: Development Install

For contributing or modifying TWM:

```bash
cd /path/to/terminal-window-management
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## Post-Installation Setup

### 1. Grant Permissions (IMPORTANT!)

On first run, you'll see an error like:
```
Python is not allowed assistive access
```

This is normal! To fix it:

1. Open **System Settings** (or System Preferences on older macOS)
2. Go to **Privacy & Security** → **Accessibility**
3. Click the lock to make changes
4. Click the **+** button and add:
   - `/usr/bin/python3` or
   - Your venv's Python: `/path/to/venv/bin/python3`
5. Also go to **Privacy & Security** → **Automation**
6. Find Python and enable **System Events** access

Alternative method:
1. Open **System Settings** → **Privacy & Security** → **Accessibility**
2. Enable **Terminal.app**

After granting permissions, TWM will work perfectly!

### 2. Test Installation

```bash
# List windows
twm list

# Show screens
twm screens

# Get help
twm --help
```

### 3. Set Up Shell Alias (Optional)

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
# Activate TWM virtual environment
alias twm-activate='source /path/to/terminal-window-management/venv/bin/activate'
```

Or add the venv to your PATH:

```bash
export PATH="/path/to/terminal-window-management/venv/bin:$PATH"
```

## Troubleshooting

### "command not found: twm"

The virtual environment isn't activated. Run:

```bash
source venv/bin/activate
```

### "externally-managed-environment" Error

You're trying to install into the system Python. Use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### PyObjC Installation Issues

If PyObjC fails to install:

1. Make sure Xcode Command Line Tools are installed:
   ```bash
   xcode-select --install
   ```

2. Update pip:
   ```bash
   pip install --upgrade pip
   ```

3. Try installing PyObjC separately:
   ```bash
   pip install PyObjC
   ```

### Permission Denied Errors

Make sure you've granted Terminal.app automation permissions in System Preferences.

### AppleScript Errors

If you get AppleScript errors:

1. Make sure Terminal.app is running
2. Check that you have at least one Terminal window open
3. Verify permissions in System Preferences

## Updating

To update TWM to the latest version:

```bash
cd /path/to/terminal-window-management
git pull  # if installed from git
source venv/bin/activate
pip install -e . --upgrade
```

## Uninstallation

### If installed with pip/venv:

```bash
source venv/bin/activate
pip uninstall twm
```

Then delete the directory:

```bash
cd ..
rm -rf terminal-window-management
```

### If installed with pipx:

```bash
pipx uninstall twm
```

## Running Tests

To verify everything is working:

```bash
source venv/bin/activate
pip install pytest
pytest tests/ -v
```

All tests should pass.

## Next Steps

- Read the [Quick Start Guide](QUICKSTART.md)
- Check out the [full documentation](README.md)
- Try the example profiles in `twm/examples/`

## Getting Help

If you encounter issues:

1. Check the [README](README.md) for common usage patterns
2. Run `twm --help` for command reference
3. Check permissions in System Preferences
4. Open an issue on GitHub with error details

Enjoy using TWM!
