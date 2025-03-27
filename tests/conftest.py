"""
Configuration file for pytest.
Contains fixtures and hooks used across multiple test files.
"""
import os
import json
import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def root_dir():
    """Return the root directory of the project."""
    return Path(__file__).parent.parent


@pytest.fixture
def test_config():
    """Return a test configuration dict."""
    return {
        "audio": {
            "sample_rate": 44100,
            "block_size": 1024,
            "channels": 1,
            "device": None
        },
        "pitch": {
            "min_confidence": 0.2,
            "min_frequency": 50,
            "max_frequency": 1000
        },
        "onset": {
            "threshold": 0.3,
            "silence": -70,
            "minimum_inter_onset_interval_ms": 80
        },
        "midi": {
            "virtual_port_name": "Test_VoiceToMIDI",
            "port_name": None
        }
    }


@pytest.fixture
def temp_config_file(test_config):
    """Create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_config, f, indent=2)
        temp_file_path = f.name
    
    yield temp_file_path
    
    # Cleanup after test
    try:
        os.unlink(temp_file_path)
    except OSError:
        pass 