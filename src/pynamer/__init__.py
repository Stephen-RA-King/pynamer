#!/usr/bin/env python3
"""Top-level package for pynamer."""

# Core Library modules
import logging.config
import pickle
from importlib.metadata import version
from importlib.resources import files
from pathlib import Path

# Third party modules
import yaml

__version__ = version("pynamer")


LOGGING_CONFIG = """
version: 1
disable_existing_loggers: True
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    stream: ext://sys.stdout
    formatter: basic
  file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    filename: logs/log.txt
    maxBytes: 1048576    # 1MB
    backupCount: 3       # keeps log.txt, log.txt.1, log.txt.2, log.txt.3
    formatter: timestamp
    encoding: utf-8


formatters:
  basic:
    style: "{"
    format: "{message:s}"
  timestamp:
    style: "{"
    format: "{asctime} - {levelname} - {filename}:{lineno} - {message}"

loggers:
  init:
    handlers: [console, file]
    level: DEBUG
    propagate: False
"""

Path("logs").mkdir(exist_ok=True)
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
    project_count = 809001


if meta_file_trv.is_file():
    meta = pickle.loads(meta_file_trv.read_bytes())
else:  # pragma: no cover
    meta = {}
