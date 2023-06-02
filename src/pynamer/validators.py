#!/usr/bin/env python3
"""Collection of functions to test availability of a package name on PyPI"""
# Core Library modules
import json
import re
import string
from datetime import datetime
from typing import Any, Union

# Third party modules
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

# Local modules
from . import logger, pypi_index_file_trv
from .config import config
from .utils import _generate_pypi_index


def _is_valid_package_name(project_name: str) -> bool:
    """Function does a basic check of project name validity.

    Args:
        project_name:   the name of the project to test.

    Returns:
        True:           If the name passes the basic check
        False:          If the name fails the basic check
    """
    pattern = r"^[a-z][_\-a-z0-9]*$"
    if re.match(pattern, project_name) is not None:
        return True
    else:
        return False


def _ping_project(project_name: str) -> bool:
    """Determines if the URL to the project exists in PyPIs project area.

    Args:
        project_name:   the name of the project to test.

    Returns:
        True:           If the URLs response code is 200
        False:          If the URLs response code is not 200

    Raises:
        SystemExit:     If any requests.RequestException occurs.
    """
    url_project = "".join([config.pypi_project_url, project_name, "/"])
    logger.debug("attempting to get url %s", url_project)
    try:
        project_ping = requests.get(url_project, timeout=5)
    except requests.RequestException as e:
        logger.error("An error occurred: %s", e)
        raise SystemExit("An error occurred with an HTTP request")
    if project_ping.status_code == 200:
        logger.debug("%s FOUND in the project area of PyPI", project_name)
        return True
    logger.debug("%s NOT FOUND in the project area of PyPI", project_name)
    return False


def _ping_json(project_name: str) -> str:
    """Collects some details about the project if it exists.

    Args:
        project_name:   the name of the project to test.

    Raises:
        SystemExit:     If any requests.RequestException occurs.
    """
    url_json = "".join([config.pypi_json_url, project_name, "/json"])
    logger.debug("attempting to get url %s", url_json)
    try:
        project_json_raw = requests.get(url_json, timeout=5)
    except requests.RequestException as e:
        logger.error("An error occurred: %s", e)
        raise SystemExit("An error occurred with an HTTP request")
    if project_json_raw.status_code == 200:
        project_json = json.loads(project_json_raw.content)
        author = (
            "".join(["Author:  ", project_json["info"]["author"]])
            if project_json["info"]["author"]
            else "Author:  None"
        )
        version = (
            "".join(["Version: ", project_json["info"]["version"]])
            if project_json["info"]["version"]
            else "Version: None"
        )
        email = (
            "".join(["Email:   ", project_json["info"]["author_email"]])
            if project_json["info"]["author_email"]
            else "Email:   None"
        )
        summary = (
            "".join(["Summary: ", project_json["info"]["summary"]])
            if project_json["info"]["summary"]
            else "Summary: None"
        )
        result = "".join([summary, "\n", author, "\n", email, "\n", version])
        return result
    logger.debug("No response from JSON URL")
    return ""


def _pypi_search_index(project_name: str) -> bool:
    """Open the generated index file and search for the project name.

    Args:
        project_name:   the name of the project currently under test.

    Returns:
        True:           A match was found.
        False:          A match was not found.
    """
    if not pypi_index_file_trv.is_file():
        _generate_pypi_index()

    projects = pypi_index_file_trv.read_text(encoding="utf-8")
    if project_name in projects:
        logger.debug("%s FOUND in the PyPI simple index", project_name)
        return True
    logger.debug("%s NOT FOUND in the PyPI simple index", project_name)
    return False


def _pypi_search(
    search_project: str,
) -> tuple[list[list[Union[str, Any]]], list[list[Union[str, Any]]], str]:
    """Performs a get request to PyPI's search API for the project name.

    Args:
        search_project:   The name of the project currently under test.

    Returns:
        match:          A list of projects matching name comprising:
                            [project_name, version, released, description]
        others:         A list of projects not matching but PyPI thinks are relevant.
                            [project_name, version, released, description]
        others_total:   A str representation of total projects found (minus matches).
    """
    pattern = re.compile(r">([\d,+]*?)<")
    s = requests.Session()
    projects_raw: list = []
    match: list[list[str]] = []
    others: list[list[str]] = []
    params = {"q": {search_project}, "page": 1}
    r = s.get(config.pypi_search_url, params=params)  # type: ignore
    soup = BeautifulSoup(r.text, "html.parser")
    projects_raw.extend(soup.select('a[class*="package-snippet"]'))
    for project_raw in projects_raw:
        project_name = project_raw.select_one(
            'span[class*="package-snippet__name"]'
        ).text.strip()
        version = project_raw.select_one(
            'span[class*="package-snippet__version"]'
        ).text.strip()
        released_iso_8601 = project_raw.select_one(
            'span[class*="package-snippet__created"]'
        ).find("time")["datetime"]
        released = datetime.strptime(released_iso_8601, "%Y-%m-%dT%H:%M:%S%z").strftime(
            "%Y-%m-%d"
        )
        description = project_raw.select_one(
            'p[class*="package-snippet__description"]'
        ).text.strip()
        if project_name.lower() == search_project.lower():
            match.append([project_name, version, released, description])
        else:
            others.append([project_name, version, released, description])

    total_div_raw = soup.select(
        'div[class="split-layout split-layout--table split-layout--wrap-on-tablet"]'
    )
    total_raw = re.search(pattern, str(total_div_raw))
    if total_raw is not None:
        total_string = total_raw.group(1)
        total = int(total_string.translate(str.maketrans("", "", string.punctuation)))
        others_total = (
            "".join([str(total), "+"])
            if total == 10000
            else (str(int(total) - len(match)))
        )
    else:
        others_total = "0"
    return match, others, others_total


def _final_analysis(pattern: list[int]) -> None:
    """Displays a rich console table displaying the conclusion of the test results

    Args:
        pattern:    A list of the test results:
                    1 - A 'negative' result, indicating the project has been found.
                    0 - A 'positive' result, indicating the project was not found.
    """
    table = Table(show_header=True)
    table.add_column("FINAL ANALYSIS", style="bold cyan")
    if pattern == [0, 1, 0]:
        table.add_row("[red]NOT AVAILABLE![/red]\n")
        table.add_row(
            "A Gotcha!, whereby the package is not found even with PyPI's own search"
            " facility.\n"
            "It can only be found by searching the simple index which is not available "
            "through the interface"
        )
    elif pattern == [1, 1, 0]:
        table.add_row("[red]NOT AVAILABLE![/red]\n")
        table.add_row(
            "A Gotcha!, whereby the package is not found even with PyPI's own search"
            " facility.\n"
            "However if appears in the simple index and can be displayed by simply"
            " browsing "
            "to the projects URL"
        )
    elif sum(pattern) >= 1:
        table.add_row("[red]NOT AVAILABLE![/red]\n")
        table.add_row("The package name was found in at least one place")
    elif sum(pattern) == 0:
        table.add_row("[green]AVAILABLE![/green]\n")
        table.add_row("The package name was not found in any part of PyPI")

    console = Console()
    console.print(table)
