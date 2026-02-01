"""Configuration management for TWM."""

import os
from pathlib import Path


def get_config_dir() -> Path:
    """Get the TWM configuration directory."""
    config_dir = Path.home() / '.config' / 'twm'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_profiles_dir() -> Path:
    """Get the profiles directory."""
    profiles_dir = get_config_dir() / 'profiles'
    profiles_dir.mkdir(parents=True, exist_ok=True)
    return profiles_dir


def get_groups_dir() -> Path:
    """Get the groups directory."""
    groups_dir = get_config_dir() / 'groups'
    groups_dir.mkdir(parents=True, exist_ok=True)
    return groups_dir


def get_config_file() -> Path:
    """Get the main configuration file path."""
    return get_config_dir() / 'config.yaml'
