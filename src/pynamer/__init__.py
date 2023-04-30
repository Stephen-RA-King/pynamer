#!/usr/bin/env python3
"""Top-level package for pynamer."""
# Core Library modules
import logging.config
import pickle
from importlib.resources import as_file, files

# Third party modules
import yaml  # type: ignore

__title__ = "pynamer"
__version__ = "0.5.0"
__author__ = "Stephen R A King"
__description__ = (
    "Utility to find an available package name on the PyPI repository and register it "
)
__email__ = "sking.github@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Stephen R A King"


LOGGING_CONFIG = """
version: 1
disable_existing_loggers: True
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    stream: ext://sys.stdout
    formatter: basic
  file:
    class: logging.FileHandler
    level: DEBUG
    filename: pynamer.log
    mode: w
    encoding: utf-8
    formatter: timestamp

formatters:
  basic:
    style: "{"
    format: "{message:s}"
  timestamp:
    style: "{"
    format: "{asctime} - {levelname} - {name} - {message}"

loggers:
  init:
    handlers: [console, file]
    level: DEBUG
    propagate: False
"""

logging.config.dictConfig(yaml.safe_load(LOGGING_CONFIG))
logger = logging.getLogger("init")

project_path = files("pynamer")

setup_file_path = project_path.joinpath("setup.txt")
with as_file(setup_file_path) as _setup_file:
    if _setup_file.exists():
        setup_text = _setup_file.read_text()
    else:
        pass
        # fix method

pickle_file_path = project_path.joinpath("project_count.pickle")
with as_file(pickle_file_path) as _pickle_file:
    if _pickle_file.exists():
        _pickle_bytes = _pickle_file.read_bytes()
        project_count = pickle.loads(_pickle_bytes)
    else:
        project_count = 449691
