#!/usr/bin/env python3
# Core Library modules
from pathlib import Path

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]

expected_result = [
    "black",
    "flake8",
    "lintilla",
    "piptools_sync",
    "pizazz",
    "pynamer",
    "pynball",
    "pynnacle",
]


def test_process_input_file(monkeypatch):
    file = str(BASE_DIR / "resources" / "input_file")
    result = pynamer._process_input_file(file)
    assert sorted(result) == expected_result
