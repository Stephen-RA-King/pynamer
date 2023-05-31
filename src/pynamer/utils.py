#!/usr/bin/env python3
"""Collection of package support utilities."""
# Core Library modules
import json
import os
import pickle
import re
from importlib.resources import as_file
from pathlib import Path
from typing import Any, Union

# Third party modules
import requests
from colorama import Back, Fore, Style
from packaging import version
from tqdm import tqdm

# First party modules
import pynamer

# Local modules
from . import logger, project_count_file_trv, pypi_index_file_trv
from .config import config


def _check_integrity() -> None:
    pass


def _reset() -> None:
    pass


def _feedback(message: str, feedback_type: str) -> None:
    """Generates a formatted messages appropriate to the message type.

    Args:
        message:        Text to be echoed.
        feedback_type:  identifies type of message to display.
    """
    if feedback_type not in ["null", "nominal", "warning", "error"]:
        return
    if config.idlemode == 1:
        print(message)
    else:
        if feedback_type == "null":
            print(Fore.WHITE + Style.BRIGHT + f"{message}" + Style.RESET_ALL)
        elif feedback_type == "nominal":
            print(Fore.GREEN + Style.BRIGHT + f"{message}" + Style.RESET_ALL)
        elif feedback_type == "warning":
            print(
                Fore.YELLOW + Back.BLACK + Style.BRIGHT + f"{message}" + Style.RESET_ALL
            )
        elif feedback_type == "error":
            print(
                Fore.RED
                + Back.BLACK
                + Style.BRIGHT
                + f"ERROR: {message}"
                + Style.RESET_ALL
            )


def _find_pypirc_file(filename: str = ".pypirc") -> None:
    """Function to iterate over paths in the PATH environment variable to find a file.

     Designed to find a .pypirc file starting with the current working directory.
     If identified will update the config.pypirc variable, so it can be used elsewhere.

    Args:
        filename:       filename to find.
    """
    system_path = os.getenv("PATH")
    if system_path is not None:
        path_directories = [os.getcwd()]
        path_directories.extend(system_path.split(os.pathsep))
        for directory in path_directories:
            file_path = Path(directory) / filename
            if file_path.exists():
                logger.debug(
                    "%s is present in the system's PATH at %s", filename, directory
                )
                config.pypirc = file_path
                break
    logger.debug("%s is not present in the system's PATH.", filename)


def _generate_pypi_index() -> None:
    """Generates a list of projects in PyPI's simple index - writes results to a file.

    Raises:
        SystemExit:     If any requests.RequestException occurs.

    Notes:
        A potentially expensive operation as there are almost 500,000 projects to
        process. Can take 2-3 seconds. Look to improve performance at a later date:
        look at asyncio, asyncio.http etc.
        An improvement is to automatically periodically run this in the background.
    """
    new_count = 0
    pattern = re.compile(r">([\w\W]*?)<")
    with as_file(pypi_index_file_trv) as pypi_index_file:
        if pypi_index_file.exists():
            pypi_index_file.unlink(missing_ok=True)

    progress_bar = tqdm(total=config.project_count)

    try:
        index_object_raw = requests.get(config.pypi_simple_index_url, timeout=5)
    except requests.RequestException as e:
        logger.error("An error occurred: %s", e)
        raise SystemExit("An error occurred with an HTTP request")
    with pypi_index_file_trv.open("a") as file:
        for line in index_object_raw.iter_lines():
            line = str(line)
            project_text = re.search(pattern, line)
            if project_text is not None:
                new_count += 1
                progress_bar.update(1)
                project = "".join([project_text.group(1), " \n"])
                file.write(project)
    progress_bar.close()
    with project_count_file_trv.open("wb") as f:
        pickle.dump(new_count, f)

    if config.project_count > 0:
        diff = new_count - config.project_count
        if diff > 0:  # pragma: no cover
            _feedback(
                f"Project count has increased by {diff} since last index generation",
                "warning",
            )
        elif diff < 0:  # pragma: no cover
            _feedback(
                f"Project count has decreased by {diff} since last index generation",
                "warning",
            )


def _check_version() -> None:
    """Utility function to compare package version against latest version on PyPI.

    Returns:
        current_version:    version of the installed package.
        str:                Message concerning the result of the comparison.
        bool:               True: if the installed package is up-to-date.
                            False: if there is a newer version on PyPI.
    """
    url_json = "".join([config.pypi_json_url, "pynamer", "/json"])
    current_version = version.parse(pynamer.__version__)
    try:
        project_json_raw = requests.get(url_json, timeout=5)
    except requests.RequestException:
        raise SystemExit("An error occurred with an HTTP request")
    if project_json_raw.status_code == 200:
        project_json = json.loads(project_json_raw.content)
        pypi_version = version.parse(project_json["info"]["version"])
        if pypi_version > current_version:
            message = f"(There is a newer version available: {pypi_version})"
            _feedback(f"{current_version} : {message}", "warning")
        elif pypi_version == current_version:
            message = "(You have the most recent version)"
            _feedback(f"{current_version} : {message}", "nominal")


def _process_input_file(file: str) -> list[Union[str, Any]]:
    """Processes the contents of the file to a list of strings.

    Args:
        file:           simple string for the file.

    Raises:
        SystemExit:     If the file is found to not exist.

    Notes:
        file contents should contain any number of space separated strings on any
        number of lines.
    """
    file_path = Path(file)
    try:
        with file_path.open(mode="r") as f:
            file_contents = f.read()
            projects = file_contents.split()
            return list(set(projects))
    except FileNotFoundError:  # pragma: no cover
        _feedback(f"The file {file} does not exist", "warning")
        raise SystemExit()
    except PermissionError:  # pragma: no cover
        _feedback(f"Permission denied to file: {file}", "warning")
        raise SystemExit()
    except IsADirectoryError:  # pragma: no cover
        _feedback(f"{file} is a directory not a file", "warning")
        raise SystemExit()
    except OSError:  # pragma: no cover
        _feedback(f"A general IO error has occurred opening file: {file}", "warning")
        raise SystemExit()
    except Exception as e:  # pragma: no cover
        _feedback(f"An error occurred:, {str(e)}", "warning")
        raise SystemExit()


def _write_output_file(file_name: str, results: dict) -> None:
    """Write the results to a file

    Args:
        file_name:      Name of file to save as a simple string.
        results:        Dictionary containing the test results e.g.
                        {"pynball": [1, 1, 1]}
    """
    header_width = 83
    truncation_width = 25
    file_path = Path(file_name)
    title = "Results from pynamer PyPI utility\n"
    title = "".join([title, "=" * header_width, "\n\n"])
    title = "".join(
        [
            title,
            "Test 1 - Basic url lookup on PyPI\n",
            "Test 2 - Search of PyPIs simple index\n",
            "Test 3 - Search using an request to PyPIs search 'API'\n\n",
        ]
    )
    header = f"{'Project':30}{'Test1':12}{'Test2':12}{'Test3':12}{'Conclusion'}\n"
    header = "".join([header, "=" * header_width, "\n"])
    projects_results: str = ""
    for project in results:
        project_name = (
            project
            if len(project) <= truncation_width
            else project[: truncation_width - 3] + "..."
        )
        projects_results = "".join([projects_results, f"{project_name:30}"])
        for test in results[project]:
            test = "Found" if test == 1 else "Not Found"
            projects_results = "".join([projects_results, f"{test:12}"])
        conclusion = "Not Available" if sum(results[project]) > 0 else "Available"
        projects_results = "".join([projects_results, f"{conclusion}"])
        projects_results = "".join([projects_results, "\n", "-" * header_width, "\n"])

    final_output_text = "".join([title, header, projects_results])

    try:  # pragma: no cover
        with file_path.open(mode="w") as f:
            f.write(final_output_text)
    except PermissionError:  # pragma: no cover
        _feedback(f"Permission denied to file: {file_path.open}", "warning")
        raise SystemExit()
    except FileExistsError:  # pragma: no cover
        _feedback(f"File {file_path.open} already exists", "warning")
        raise SystemExit()
    except IsADirectoryError:  # pragma: no cover
        _feedback(f"{file_path.open} is a directory not a file", "warning")
        raise SystemExit()
    except OSError:  # pragma: no cover
        _feedback("General IO error has occurred", "warning")
        raise SystemExit()
    except Exception as e:  # pragma: no cover
        _feedback(f"An error occurred:, {str(e)}", "warning")
        raise SystemExit()
