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

setup(name='pynamer',
      version='0.0.0',
      description='place holder',
      url='http://github.com/SK/pynamer',
      author='sking',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['pynamer'],
      zip_safe=False)"""


def test_create_setup(create_env, project_path_mock):
    pynamer._create_setup("pynamer")
    setup_file = BASE_DIR / "setup.py"
    with open(setup_file, encoding="utf-8") as f:
        contents = f.read()
    assert contents == expected_content

    setup_file.unlink()
