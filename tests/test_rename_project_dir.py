#!/usr/bin/env python3
# Core Library modules
from pathlib import Path

# Third party modules
import pytest

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]


def test_rename_directory(create_env):
    old_name = BASE_DIR / "project_name"
    new_name = BASE_DIR / "pynamer"
    assert old_name.exists()
    pynamer._rename_project_dir(old_name, new_name)
    assert new_name.exists()
    pynamer._rename_project_dir(new_name, old_name)


def test_rename_directory_dir_missing(create_env):
    old_name = BASE_DIR / "project_name1"
    new_name = BASE_DIR / "pynamer"
    with pytest.raises(FileNotFoundError):
        pynamer._rename_project_dir(old_name, new_name)
