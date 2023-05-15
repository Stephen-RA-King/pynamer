#!/usr/bin/env python3
# Core Library modules
from pathlib import Path

# Third party modules
import pytest

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]
expected_content = """#!/usr/bin/env python3


# Third party modules
from setuptools import setup

setup(name='pynball',
      version='0.0.0',
      description='place holder',
      url='http://github.com/SK/pynball',
      author='sking',
      author_email='sking@gmail.com',
      license='MIT',
      packages=['pynball'],
      zip_safe=False)"""


def test_create_setup(create_env, project_path_mock, monkeypatch):
    inputs = iter(["sking", "sking@gmail.com"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    pynamer._create_setup("pynball")
    setup_file = BASE_DIR / "setup.py"
    with open(setup_file, encoding="utf-8") as f:
        contents = f.read()
    assert contents == expected_content

    setup_file.unlink()
