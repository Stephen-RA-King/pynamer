#!/usr/bin/env python3
# Core Library modules
import pickle
from pathlib import Path

# Third party modules
import pytest
import requests
from requests.exceptions import ConnectTimeout

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]


def my_custom_get_found(url, **kwargs):
    _pickle_file = BASE_DIR / "resources" / "requests_get_ping_pynball.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def my_custom_get_not_found(url, **kwargs):
    _pickle_file = BASE_DIR / "resources" / "requests_get_ping_zeedonk.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def test_ping_project_found(monkeypatch):
    monkeypatch.setattr(requests, "get", my_custom_get_found)
    result = pynamer._ping_project("pynball")
    assert result is True


def test_ping_project_not_found(monkeypatch):
    monkeypatch.setattr(requests, "get", my_custom_get_not_found)
    result = pynamer._ping_project("zeedonk")
    assert result is False


def test_ping_project_error(monkeypatch):
    def mock_requests_error(*args, **kwargs):
        raise ConnectTimeout("Connection timed out")

    monkeypatch.setattr(requests, "get", mock_requests_error)

    with pytest.raises(SystemExit) as excinfo:
        pynamer._ping_project("pynball")
    assert str(excinfo.value) == "An error occurred with an HTTP request"
