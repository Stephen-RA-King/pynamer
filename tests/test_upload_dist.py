#!/usr/bin/env python3
# Core Library modules
import os
import sys
from pathlib import Path

# Third party modules
import pytest

# First party modules
from pynamer import pynamer

BASE_DIR = Path(__file__).parents[0]


def test_dist_upload(monkeypatch, project_path_mock, capsys):
    captured_args = []
    python_path = str(sys.executable)
    pypirc_path = os.fspath(BASE_DIR / ".pypirc")
    dist_path = os.fspath(BASE_DIR / "dist" / "*")

    def mock_run_command(*args, **kwargs):
        captured_args.extend(args)
        return args

    monkeypatch.setattr(pynamer, "_run_command", mock_run_command)
    monkeypatch.setattr(pynamer.config, "pypirc", pypirc_path)

    pynamer._upload_dist("pynball")

    assert captured_args == [
        python_path,
        "-m",
        "twine",
        "upload",
        "--config-file",
        pypirc_path,
        dist_path,
    ]
