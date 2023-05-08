#!/usr/bin/env python3
# Core Library modules
import pickle
from pathlib import Path

# Third party modules
import pytest
import requests

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]


def my_custom_get(url, **kwargs):
    _pickle_file = BASE_DIR / "resources" / "ping_pynball.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def test_ping_project(monkeypatch):
    monkeypatch.setattr(requests, "get", my_custom_get)
    result = pynamer._ping_project("pynball")
    assert result is True
