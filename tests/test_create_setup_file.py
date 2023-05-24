#!/usr/bin/env python3
# Core Library modules
from pathlib import Path

# First party modules
from pynamer import builder, pynamer

BASE_DIR = Path(__file__).parents[0]
expected_content = """#!/usr/bin/env python3


# Third party modules
from setuptools import setup

setup(name='pynball',
      version='0.0.1',
      description='a new project',
      url='http://github.com/SK/pynball',
      author='sking',
      author_email='sking@gmail.com',
      license='MIT',
      packages=['pynball'],
      zip_safe=False)"""


def test_create_setup(create_env, monkeypatch):
    inputs = iter(["sking", "sking@gmail.com", "0.0.1", "a new project"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr(builder, "project_path", BASE_DIR)
    monkeypatch.setattr(builder, "setup_file_trv", BASE_DIR / "setup.txt")
    monkeypatch.setattr(builder, "setup_file_py_trv", BASE_DIR / "setup.py")
    monkeypatch.setattr(builder, "meta_file_trv", BASE_DIR / "meta.pickle")

    builder._create_setup("pynball")

    setup_file = BASE_DIR / "setup.py"
    with open(setup_file, encoding="utf-8") as f:
        contents = f.read()
    assert contents == expected_content

    setup_file.unlink()
