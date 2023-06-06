#!/usr/bin/env python3
# Core Library modules
import pickle
from pathlib import Path

# Third party modules
import pytest
import requests
from requests.exceptions import ConnectTimeout

# First party modules
from pynamer import pynamer, validators

BASE_DIR = Path(__file__).parents[0]

expected_response_found = """Summary:  Utility command line tool to manage python versions
Author:   Stephen R A King
Email:    sking.github@gmail.com
Version:  1.5.5
Homepage: https://github.com/stephen-ra-king/pynball"""


expected_response_found_stats = """Summary:  Utility command line tool to manage python versions
Author:   Stephen R A King
Email:    sking.github@gmail.com
Version:  1.5.5
Homepage: https://github.com/stephen-ra-king/pynball

GitHub Stats
------------
stars:    1
forks:    0
license:  MIT License
watching: 2
created:  2022-02-28
updated:  2023-05-22"""


def return_stats(url, **kwargs):
    stats = """

GitHub Stats
------------
stars:    1
forks:    0
license:  MIT License
watching: 2
created:  2022-02-28
updated:  2023-05-22"""
    return stats


def my_custom_get_found(url, **kwargs):
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


def test_ping_json_found_stats1(monkeypatch):
    monkeypatch.setattr(requests, "get", my_custom_get_found)
    monkeypatch.setattr(validators, "_github_meta", return_stats)
    result = pynamer._ping_json("pynball", stats=True)
    assert result == expected_response_found_stats
