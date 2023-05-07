#!/usr/bin/env python3
# Core Library modules
from pathlib import Path

# Third party modules
import pytest

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]


def test_delete_director():
    command = ["echo", "Hello, World!"]
    expected_output = None
    result = pynamer._run_command(command, capture_output=True, text=True)
    assert result == expected_output
