#!/usr/bin/env python3
# Core Library modules
import platform
from pathlib import Path

# First party modules
from pynamer import builder, pynamer

OS = platform.system()
BASE_DIR = Path(__file__).parents[0]


def test_project_path():
    if OS == "Windows":
        assert str(pynamer.project_path).endswith("pynamer\\src\\pynamer")
    else:
        assert str(pynamer.project_path).endswith("pynamer/src/pynamer")


def test_project_count(project_path_mock):
    assert pynamer.project_count >= 452490


def test_setup_text():
    assert (
        builder.setup_text
        == """#!/usr/bin/env python3


# Third party modules
from setuptools import setup

setup(name='{{ PROJECT_NAME }}',
      version='{{ PACKAGE_VERSION }}',
      description='{{ DESCRIPTION }}',
      url='http://github.com/SK/{{ PROJECT_NAME }}',
      author='{{ AUTHOR }}',
      author_email='{{ EMAIL }}',
      license='MIT',
      packages=['{{ PROJECT_NAME }}'],
      zip_safe=False)
"""
    )


def test_defaults():
    assert pynamer.config.pypirc is None
    assert pynamer.config.original_project_name == "project_name"
    assert pynamer.config.no_cleanup is False
    assert pynamer.config.package_version == "0.0.0"
    assert pynamer.config.pypi_search_url == "https://pypi.org/search/"
    assert pynamer.config.pypi_project_url == "https://pypi.org/project/"
    assert pynamer.config.pypi_json_url == "https://pypi.org/pypi/"
    assert pynamer.config.pypi_simple_index_url == "https://pypi.org/simple/"
    assert pynamer.config.idlemode == 0
