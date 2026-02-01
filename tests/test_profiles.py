"""Tests for profile management."""

import pytest
from pydantic import ValidationError
from twm.profiles import WindowConfig, Profile


def test_window_config_creation():
    """Test WindowConfig creation."""
    config = WindowConfig(
        position={'x': 0, 'y': 23, 'width': 1920, 'height': 1080},
        title='Test Window',
        theme='Pro'
    )
    assert config.position['x'] == 0
    assert config.title == 'Test Window'
    assert config.theme == 'Pro'


def test_profile_creation():
    """Test Profile creation with windows."""
    window1 = WindowConfig(
        position={'x': 0, 'y': 23, 'width': 960, 'height': 1080}
    )
    window2 = WindowConfig(
        position={'x': 960, 'y': 23, 'width': 960, 'height': 1080}
    )

    profile = Profile(
        name='test',
        description='Test profile',
        windows=[window1, window2]
    )

    assert profile.name == 'test'
    assert profile.description == 'Test profile'
    assert len(profile.windows) == 2


def test_profile_serialization():
    """Test profile serialization to dict."""
    window = WindowConfig(
        position={'x': 0, 'y': 23, 'width': 1920, 'height': 1080},
        title='Test'
    )

    profile = Profile(
        name='test',
        windows=[window]
    )

    data = profile.model_dump()
    assert data['name'] == 'test'
    assert len(data['windows']) == 1
    assert data['windows'][0]['position']['x'] == 0
