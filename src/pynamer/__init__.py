#!/usr/bin/env python3
"""Top-level package for pynamer."""
# Core Library modules
import logging.config
import pickle
from importlib.resources import as_file, files

# Third party modules
import yaml  # type: ignore

__title__ = "pynamer"
__version__ = "1.0.0"
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


formatters:
  basic:
    style: "{"
    format: "{message:s}"
  timestamp:
    style: "{"
    format: "{asctime} - {levelname} - {name} - {message}"

loggers:
  init:
    handlers: []
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


project_count_file_path = project_path.joinpath("project_count.pickle")
with as_file(project_count_file_path) as _project_count_file:
    if _project_count_file.exists():
        _project_count_bytes = _project_count_file.read_bytes()
        project_count = pickle.loads(_project_count_bytes)
    else:
        project_count = 452490


meta_file_path = project_path.joinpath("meta.pickle")
with as_file(meta_file_path) as _meta_file:
    if _meta_file.exists():
        _meta_bytes = _meta_file.read_bytes()
        meta = pickle.loads(_meta_bytes)
    else:
        meta = {}
