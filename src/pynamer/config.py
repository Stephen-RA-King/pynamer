#!/usr/bin/env python3

# Core Library modules
import sys
from pathlib import Path
from typing import Optional

# Local modules
from . import project_count, project_path


class Config:
    """Configuration class"""

    pypirc: Optional[Path] = None
    original_project_name: str = "project_name"
    no_cleanup: bool = False
    project_count: int = project_count
    package_version: str = "0.0.0"
    pypi_search_url: str = "https://pypi.org/search/"
    pypi_project_url: str = "https://pypi.org/project/"
    pypi_json_url: str = "https://pypi.org/pypi/"
    pypi_simple_index_url: str = "https://pypi.org/simple/"
    idlemode: int = 1 if "idlelib.run" in sys.modules else 0


config = Config()
