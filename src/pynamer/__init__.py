#!/usr/bin/env python3
"""Top-level package for pynamer."""
# Core Library modules
import logging.config
import pickle
from importlib.resources import files

# Third party modules
import yaml

__title__ = "pynamer"
__version__ = "2.1.8"
__author__ = "Stephen R A King"
__description__ = (
    "Utility to find an available package name in the PyPI repository and register it "
)
__email__ = "sking.github@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Stephen R A King"
__all__ = ["builder", "cli", "config", "pynamer", "utils", "validators"]


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
setup_file_trv = project_path.joinpath("setup.txt")
setup_file_py_trv = project_path.joinpath("setup.py")
setup_base_file_trv = project_path.joinpath("setup_base.txt")
project_count_file_trv = project_path.joinpath("project_count.pickle")
pypi_index_file_trv = project_path.joinpath("pypi_index")
meta_file_trv = project_path.joinpath("meta.pickle")


if setup_file_trv.is_file():
    setup_text = setup_file_trv.read_text(encoding="utf-8")
else:  # pragma: no cover
    raise SystemExit("The package has a structural problem")


if project_count_file_trv.is_file():
    project_count = pickle.loads(project_count_file_trv.read_bytes())
else:  # pragma: no cover
    project_count = 472729


if meta_file_trv.is_file():
    meta = pickle.loads(meta_file_trv.read_bytes())
else:  # pragma: no cover
    meta = {}
