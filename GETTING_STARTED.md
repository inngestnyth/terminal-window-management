# Getting Started with TWM

Quick guide to get TWM up and running in 2 minutes.

## Installation (3 steps)

### Step 1: Create Virtual Environment and Install

```bash
cd "Terminal Window Management"
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

You should see "Successfully installed twm-0.1.0" at the end.

### Step 2: Verify Installation

```bash
twm --version
```

Should show: `twm, version 0.1.0`

### Step 3: Grant Permissions

When you first try to use TWM, you'll see an error:
```
Python is not allowed assistive access
```

**Fix this by:**

1. Open **System Settings** (macOS Ventura+) or **System Preferences** (older macOS)
2. Navigate to **Privacy & Security** → **Accessibility**
3. Click the 🔒 lock icon to make changes
4. Click the **+** button
5. Add your Python executable:
   - Easy way: `/usr/bin/python3`
   - Or your venv: `/path/to/Terminal Window Management/venv/bin/python3`
6. Enable the checkbox next to Python

**Also enable in Automation:**
1. **Privacy & Security** → **Automation**
2. Find **Python** in the list
3. Enable **System Events**

### Step 4: Test It Works

```bash
twm list
```

If you see your terminal windows listed, you're all set! 🎉

## First Commands to Try

```bash
# List all terminal windows
twm list

# Move current window to left half
twm left

# Move current window to right half
twm right

# Arrange 4 windows in a 2x2 grid
twm grid 2x2

# See all available themes
twm color list-themes

# Apply a theme
twm color theme Pro

# Set tab color
twm color tab blue

# Save your current layout
twm profile save my-workspace

# Show all commands
twm --help
```

## Activation for Future Sessions

Each time you open a new terminal session, activate the venv:

```bash
cd "Terminal Window Management"
source venv/bin/activate
```

Or add this alias to your `~/.zshrc` or `~/.bashrc`:

```bash
alias twm-activate='cd "/Users/yourusername/path/to/Terminal Window Management" && source venv/bin/activate'
```

Then just run `twm-activate` to start using TWM.

## Next Steps

- Read [QUICKSTART.md](QUICKSTART.md) for common workflows
- See [README.md](README.md) for complete documentation
- Check `twm/examples/` for example profiles
- Try `twm profile list` to see available profiles

## Troubleshooting

### "command not found: twm"
→ Activate the virtual environment: `source venv/bin/activate`

### "Python is not allowed assistive access"
→ Follow Step 3 above to grant permissions

### "No Terminal windows found"
→ Make sure Terminal.app has at least one window open

### Still having issues?
→ Check [INSTALL.md](INSTALL.md) for detailed troubleshooting

Happy window managing! 🪟
