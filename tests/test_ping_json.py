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

expected_response_found = """Stephen R A King
sking.github@gmail.com
1.5.5
Utility command line tool to manage python versions"""


def my_custom_get_found(url, **kwargs):
    # Implement your custom logic here
    _pickle_file = BASE_DIR / "resources" / "requests_get_json_pynball.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def my_custom_get_not_found(url, **kwargs):
    _pickle_file = BASE_DIR / "resources" / "requests_get_json_zeedonk.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def test_ping_json_found(monkeypatch):
    monkeypatch.setattr(requests, "get", my_custom_get_found)
    result = pynamer._ping_json("pynball")
    assert result == expected_response_found


def test_ping_json_not_found(monkeypatch):
    monkeypatch.setattr(requests, "get", my_custom_get_not_found)
    result = pynamer._ping_json("zeedonk")
    assert result == ""


def test_ping_json_error(monkeypatch):
    def mock_requests_error(*args, **kwargs):
        raise ConnectTimeout("Connection timed out")

    monkeypatch.setattr(requests, "get", mock_requests_error)

    with pytest.raises(SystemExit) as excinfo:
        pynamer._ping_json("pynball")
    assert str(excinfo.value) == "An error occurred with an HTTP request"
