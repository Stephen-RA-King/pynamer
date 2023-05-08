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


match_expected = [
    [
        "pynball",
        "1.5.5",
        "2023-04-21",
        "Utility command line tool to manage python versions",
    ],
]

others_expected = [
    [
        "pynamer",
        "0.5.5",
        "2023-05-03",
        "Utility to find an available package name on the PyPI repository and register it",
    ],
]


def my_custom_get(url, *args, **kwargs):
    _pickle_file = BASE_DIR / "resources" / "search_pynball.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def test_pypi_search_index(monkeypatch):
    monkeypatch.setattr(requests.Session, "get", my_custom_get)
    match, others, others_total = pynamer._pypi_search("pynball")
    assert match == match_expected
    assert others == others_expected
    assert others_total == "1"
