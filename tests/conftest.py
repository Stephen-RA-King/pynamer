# Core Library modules
import os
import pickle
import shutil
from pathlib import Path

# Third party modules
import pytest
from requests.exceptions import ConnectTimeout

# First party modules
from pynamer import project_path, pynamer

BASE_DIR = Path(__file__).parents[0]

setup_text = """#!/usr/bin/env python3


# Third party modules
from setuptools import setup

setup(name='{{ PROJECT_NAME }}',
      version='{{ PACKAGE_VERSION }}',
      description='place holder',
      url='http://github.com/SK/{{ PROJECT_NAME }}',
      author='{{ AUTHOR }}',
      author_email='{{ EMAIL }}',
      license='MIT',
      packages=['{{ PROJECT_NAME }}'],
      zip_safe=False)"""


@pytest.fixture()
def create_env(monkeypatch):
    project_dir = BASE_DIR / "project_name"
    project_dir.mkdir()
    project_init_file = BASE_DIR / "project_name" / "__init__.py"
    project_init_file.touch()
    setup_file = BASE_DIR / "setup.txt"
    setup_file.touch()
    setup_file.write_text(setup_text)
    setup_base_file = BASE_DIR / "setup_base.txt"
    setup_base_file.touch()
    setup_base_file.write_text(setup_text)
    pypirc_file = BASE_DIR / ".pypirc"
    pypirc_file.touch()
    setup_py = BASE_DIR / "setup.py"
    meta = BASE_DIR / "meta.pickle"

    yield

    manifest = [project_dir, setup_file, setup_base_file, pypirc_file, setup_py, meta]
    for item in manifest:
        if item.exists():
            if item.is_dir():
                shutil.rmtree(item)
            elif item.is_file():
                item.unlink()


@pytest.fixture()
def path_mock(mocker):
    mocker.patch.dict(os.environ, {"PATH": str(BASE_DIR)})
    mocker.patch("os.getcwd", return_value=str(BASE_DIR))


@pytest.fixture()
def project_path_mock(monkeypatch):
    monkeypatch.setattr(pynamer, "project_path", BASE_DIR)


@pytest.fixture
def mock_ping_project(monkeypatch):
    def mocked_ping_project(*args, **kwargs):
        return "_ping_project function was called"

    monkeypatch.setattr(pynamer, "_ping_project", mocked_ping_project)


@pytest.fixture
def mock_cleanup(monkeypatch):
    def mocked_cleanup(*args, **kwargs):
        return "_cleanup function was called"

    monkeypatch.setattr(pynamer, "_cleanup", mocked_cleanup)
