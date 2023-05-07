#!/usr/bin/env python3
# Core Library modules
import pickle
import platform
from pathlib import Path

# Third party modules
import pytest

# First party modules
from pynamer import pynamer

operating_system = platform.system()
BASE_DIR = Path(__file__).parents[0]


@pytest.fixture()
def create_pkl_object(monkeypatch):
    pypi_count = BASE_DIR / "project_count.pickle"
    with open(pypi_count, "wb") as f:
        pickle.dump(449692, f)
    # monkeypatch.setattr('pynamer.pickle_file_path', BASE_DIR / "project_count.pickle")
    # monkeypatch.setattr('pynamer.Path', lambda path: pypi_count)
    monkeypatch.setattr(pynamer, "pickle_file_path", BASE_DIR / "project_count.pickle")
    yield
    pypi_count.unlink()


def test_project_path():
    if operating_system == "Windows":
        assert str(pynamer.project_path).endswith("pynamer\\src\\pynamer")
    else:
        assert str(pynamer.project_path).endswith("pynamer/src/pynamer")


def test_project_count():
    assert pynamer.project_count == 449691


def test_setup_text():
    assert (
        pynamer.setup_text
        == """#!/usr/bin/env python3


# Third party modules
from setuptools import setup

setup(name='{{ PROJECT_NAME }}',
      version='{{ PACKAGE_VERSION }}',
      description='place holder',
      url='http://github.com/SK/{{ PROJECT_NAME }}',
      author='sking',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['{{ PROJECT_NAME }}'],
      zip_safe=False)
"""
    )


def test_defaults():
    assert pynamer.config.original_project_name == "project_name"
    assert pynamer.config.no_cleanup is False
    assert pynamer.config.project_count == 449691
    assert pynamer.config.package_version == "0.0.0"
    assert pynamer.config.pypi_search_url == "https://pypi.org/search/"
    assert pynamer.config.pypi_project_url == "https://pypi.org/project/"
    assert pynamer.config.pypi_json_url == "https://pypi.org/pypi/"
    assert pynamer.config.pypi_simple_index_url == "https://pypi.org/simple/"
    assert pynamer.config.idlemode == 0
