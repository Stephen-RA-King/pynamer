#!/usr/bin/env python3
# Core Library modules
import json
import pickle
from pathlib import Path

# First party modules
import pynamer

BASE_DIR = Path(__file__).parents[0]


def test_search_json_black():
    pickle_file = BASE_DIR / "resources" / "requests_get_json_black.pickle"
    pickle_bytes = pickle_file.read_bytes()
    request_object = pickle.loads(pickle_bytes)
    project_json = json.loads(request_object.content)

    url = pynamer.utils._search_json(project_json, "black")

    assert url == "https://github.com/psf/black"


def test_search_json_isort():
    pickle_file = BASE_DIR / "resources" / "requests_get_json_isort.pickle"
    pickle_bytes = pickle_file.read_bytes()
    request_object = pickle.loads(pickle_bytes)
    project_json = json.loads(request_object.content)

    url = pynamer.utils._search_json(project_json, "isort")

    assert url == "https://github.com/pycqa/isort"


def test_search_json_requests():
    pickle_file = BASE_DIR / "resources" / "requests_get_json_requests.pickle"
    pickle_bytes = pickle_file.read_bytes()
    request_object = pickle.loads(pickle_bytes)
    project_json = json.loads(request_object.content)

    url = pynamer.utils._search_json(project_json, "requests")

    assert url == "https://github.com/psf/requests"
