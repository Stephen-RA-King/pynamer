#!/usr/bin/env python3
# Core Library modules
import os
from pathlib import Path

# Third party modules
import pytest

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]


def test_find_pypirc(create_env, path_mock):
    assert pynamer.config.pypirc is None
    assert os.environ["PATH"] == str(BASE_DIR)
    pynamer._find_pypirc_file()
    assert pynamer.config.pypirc == BASE_DIR / ".pypirc"
    pynamer.config.pypirc = None


def test_find_pypirc_missing_file(create_env, path_mock):
    assert pynamer.config.pypirc is None
    assert os.environ["PATH"] == str(BASE_DIR)
    pypirc_file = BASE_DIR / ".pypirc"
    pypirc_file.unlink()
    pynamer._find_pypirc_file()
    assert pynamer.config.pypirc is None
