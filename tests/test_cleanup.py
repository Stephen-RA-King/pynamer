#!/usr/bin/env python3
# Core Library modules
import shutil
from pathlib import Path

# Third party modules
import pytest

# First party modules
from pynamer import builder, pynamer

BASE_DIR = Path(__file__).parents[0]


@pytest.fixture()
def pre_cleanup(monkeypatch):
    project_dir = BASE_DIR / "pynamer"
    project_dir.mkdir()
    build_dir = BASE_DIR / "build"
    build_dir.mkdir()
    dist_dir = BASE_DIR / "dist"
    dist_dir.mkdir()
    egg_dir = BASE_DIR / "pynamer.egg-info"
    egg_dir.mkdir()
    setup_py = BASE_DIR / "setup.py"
    setup_py.touch()

    yield

    if (BASE_DIR / "project_name").exists():
        shutil.rmtree(BASE_DIR / "project_name")


def test_cleanup(pre_cleanup, monkeypatch):
    monkeypatch.setattr(builder, "project_path", BASE_DIR)
    pynamer._cleanup("pynamer")
    assert not (BASE_DIR / "build").exists()
    assert not (BASE_DIR / "dist").exists()
    assert not (BASE_DIR / "dist" / "pynamer-0.0.0.tar.gz").exists()
    assert not (BASE_DIR / "dist" / "pynamer-0.0.0-py3-none-any.whl").exists()
    assert not (BASE_DIR / "pynamer.egg-info").exists()
