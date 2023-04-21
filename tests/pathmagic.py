#!/usr/bin/env python3
"""Utility script to add module location to sys path."""

# Core Library modules
import pathlib
import sys

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
SRC = BASE_DIR / "src"
sys.path.insert(0, str(SRC))
