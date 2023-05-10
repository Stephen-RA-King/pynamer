#!/usr/bin/env python3
# Core Library modules

# Core Library modules
import platform

# First party modules
from pynamer import pynamer


def test_default_args():
    parser = pynamer._parse_args([])
    assert parser.projects == "None"
    assert parser.register is False
    assert parser.dryrun is False
    assert parser.file == "None"
    assert parser.output == "None"
    assert parser.nocleanup is False
    assert parser.verbose is False
    assert parser.generate is False


def test_args_project():
    parser = pynamer._parse_args(
        [
            "pynball",
        ]
    )
    assert parser.projects == ["pynball"]


def test_args_projects():
    parser = pynamer._parse_args(
        [
            "pynball",
            "pizazz",
        ]
    )
    assert parser.projects == ["pynball", "pizazz"]


def test_args_register():
    parser = pynamer._parse_args(
        [
            "-r",
        ]
    )
    assert parser.register is True


def test_args_dryrun():
    parser = pynamer._parse_args(
        [
            "-d",
        ]
    )
    assert parser.dryrun is True


def test_args_file():
    parser = pynamer._parse_args(["-f", "input_file"])
    assert parser.file == "input_file"


def test_args_output():
    parser = pynamer._parse_args(["-o", "output_file"])
    assert parser.output == "output_file"


def test_args_nocleanup():
    parser = pynamer._parse_args(
        [
            "-n",
        ]
    )
    assert parser.nocleanup is True


def test_args_verbose():
    parser = pynamer._parse_args(
        [
            "-v",
        ]
    )
    assert parser.verbose is True


def test_args_generate():
    parser = pynamer._parse_args(
        [
            "-g",
        ]
    )
    assert parser.generate is True
