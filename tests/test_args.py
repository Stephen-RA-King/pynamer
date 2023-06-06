#!/usr/bin/env python3
# Core Library modules

# Core Library modules


# First party modules
from pynamer import pynamer


def test_default_args():
    args, parser = pynamer._parse_args([])
    assert args.projects == "None"
    assert args.register is False
    assert args.dryrun is False
    assert args.file == "None"
    assert args.output == "None"
    assert args.nocleanup is False
    assert args.verbose is False
    assert args.generate is False


def test_args_project():
    args, parser = pynamer._parse_args(
        [
            "pynball",
        ]
    )
    assert args.projects == ["pynball"]


def test_args_projects():
    args, parser = pynamer._parse_args(
        [
            "pynball",
            "pizazz",
        ]
    )
    assert args.projects == ["pynball", "pizazz"]


def test_args_register():
    args, parser = pynamer._parse_args(
        [
            "-r",
        ]
    )
    assert args.register is True


def test_args_dryrun():
    args, parser = pynamer._parse_args(
        [
            "-d",
        ]
    )
    assert args.dryrun is True


def test_args_file():
    args, parser = pynamer._parse_args(["-f", "input_file"])
    assert args.file == "input_file"


def test_args_output():
    args, parser = pynamer._parse_args(["-o", "output_file"])
    assert args.output == "output_file"


def test_args_nocleanup():
    args, parser = pynamer._parse_args(
        [
            "-n",
        ]
    )
    assert args.nocleanup is True


def test_args_verbose():
    args, parser = pynamer._parse_args(
        [
            "-v",
        ]
    )
    assert args.verbose is True


def test_args_generate():
    args, parser = pynamer._parse_args(
        [
            "-g",
        ]
    )
    assert args.generate is True


def test_args_webbrowser():
    args, parser = pynamer._parse_args(
        [
            "-w",
        ]
    )
    assert args.webbrowser is True


def test_args_stats():
    args, parser = pynamer._parse_args(
        [
            "-s",
        ]
    )
    assert args.stats is True
