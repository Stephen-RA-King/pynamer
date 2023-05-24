#!/usr/bin/env python3
# Core Library modules
import shutil
from pathlib import Path

# Third party modules
import pytest

# First party modules
from pynamer import builder, pynamer

BASE_DIR = Path(__file__).parents[0]

setup_text = """#!/usr/bin/env python3

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


@pytest.fixture()
def pre_build_dist(monkeypatch):
    project_dir = BASE_DIR / "pynamer"
    project_dir.mkdir()
    project_init_file = BASE_DIR / "pynamer" / "__init__.py"
    project_init_file.touch()
    pypirc_file = BASE_DIR / ".pypirc"
    pypirc_file.touch()
    setup_py = BASE_DIR / "setup.py"
    setup_py.touch()
    setup_py.write_text(setup_text)
    readme_file = BASE_DIR / "README.md"
    readme_file.touch()
    readme_file.write_text("pynamer")
    build = BASE_DIR / "build"
    dist = BASE_DIR / "dist"
    egg = BASE_DIR / "pynamer.egg-info"

    yield

    manifest = [
        project_dir,
        pypirc_file,
        setup_py,
        readme_file,
        build,
        dist,
        egg,
    ]
    for item in manifest:
        if item.exists():
            if item.is_dir():
                shutil.rmtree(item)
            elif item.is_file():
                item.unlink()


@pytest.mark.slow
def test_build_dist(pre_build_dist, monkeypatch):
    # monkeypatch.setattr(pynamer, "project_path", BASE_DIR)
    monkeypatch.setattr(builder, "project_path", BASE_DIR)
    pynamer._build_dist()
    # builder._build_dist()
    assert (BASE_DIR / "build").exists()
    assert (BASE_DIR / "dist").exists()
    assert (BASE_DIR / "dist" / "pynamer-0.0.0.tar.gz").exists()
    assert (BASE_DIR / "dist" / "pynamer-0.0.0-py3-none-any.whl").exists()
    assert (BASE_DIR / "pynamer.egg-info").exists()
