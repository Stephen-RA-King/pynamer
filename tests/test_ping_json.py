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

expected_response = """Stephen R A King
sking.github@gmail.com
1.5.5
Utility command line tool to manage python versions"""


def my_custom_get(url, **kwargs):
    # Implement your custom logic here
    _pickle_file = BASE_DIR / "resources" / "json_pynball.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def test_ping_json(monkeypatch):
    monkeypatch.setattr(requests, "get", my_custom_get)
    result = pynamer._ping_json("pynball")
    assert result == expected_response
