#!/usr/bin/env python3
# Core Library modules
import pickle
import shutil
from pathlib import Path

# Third party modules
import pytest
import requests

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]


def my_custom_get(url, **kwargs):
    _pickle_file = BASE_DIR / "resources" / "simple_index.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def test_ping_json(monkeypatch, project_path_mock):
    monkeypatch.setattr(requests, "get", my_custom_get)
    pynamer._generate_pypi_index()
    assert (BASE_DIR / "pypi_index").exists()
    assert (BASE_DIR / "project_count.pickle").exists()
    (BASE_DIR / "pypi_index").unlink()
    (BASE_DIR / "project_count.pickle").unlink()
