#!/usr/bin/env python3
# Core Library modules
from pathlib import Path

# First party modules
from pynamer import builder, pynamer

BASE_DIR = Path(__file__).parents[0]


def test_delete_director(create_env):
    project_dir = BASE_DIR / "project_name"
    setup_file = BASE_DIR / "setup.txt"
    pypirc_file = BASE_DIR / ".pypirc"
    items_to_delete = [project_dir, setup_file, pypirc_file, BASE_DIR / "hello.txt"]
    builder._delete_director(items_to_delete)
    for item in items_to_delete:
        assert not item.exists()
