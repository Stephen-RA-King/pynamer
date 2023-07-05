#!/usr/bin/env python3
# Core Library modules
import pickle
from pathlib import Path

# Third party modules
import pytest
import requests
from requests.exceptions import ConnectTimeout

# First party modules
import pynamer

BASE_DIR = Path(__file__).parents[0]


expected_response_found = """

GitHub Stats
------------
stars:    32616
forks:    2102
issues:   405
license:  MIT License
watching: 229
created:  2018-03-14
updated:  2023-06-12"""


expected_response_http_error = """

GitHub Stats
------------
GitHub can not be contacted"""


expected_response_404_error = """

GitHub Stats
------------
JSON API Does not exist.\nThis usually indicates a very old repository."""


@pytest.fixture
def mock_response_404(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 404

            def json(self):
                return {}

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


def my_custom_get_found(url, **kwargs):
    _pickle_file = BASE_DIR / "resources" / "requests_get_github_json_black.pickle"
    _pickle_bytes = _pickle_file.read_bytes()
    pickle_content = pickle.loads(_pickle_bytes)
    return pickle_content


def test_github_meta_black(monkeypatch):
    monkeypatch.setattr(requests, "get", my_custom_get_found)
    result = pynamer.validators.github_meta("https://github.com/psf/black")
    assert result == expected_response_found


def test_ping_json_error(monkeypatch):
    def mock_requests_error(*args, **kwargs):
        raise ConnectTimeout("Connection timed out")

    monkeypatch.setattr(requests, "get", mock_requests_error)

    result = pynamer.validators.github_meta("https://github.com/psf/black")
    assert result == expected_response_http_error


def test_ping_json_not_exist(mock_response_404):
    result = pynamer.validators.github_meta("https://github.com/psf/black")
    assert result == expected_response_404_error
