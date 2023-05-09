#!/usr/bin/env python3

# Core Library modules
import argparse
import json
import logging
import os
import pickle
import re
import shutil
import string
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

# Third party modules
import build
import requests
from bs4 import BeautifulSoup
from colorama import Back, Fore, Style
from jinja2 import Template
from rich.console import Console
from rich.table import Table
from tqdm import tqdm

# Local modules
from . import project_count, project_path, setup_text

logger = logging.getLogger()
for handler in logger.handlers:
    logger.removeHandler(handler)


class Config:
    """Configuration class"""

    pypirc: Optional[Path] = None
    original_project_name = "project_name"
    no_cleanup: bool = False
    project_count = 0
    package_version = "0.0.0"
    pypi_search_url: str = "https://pypi.org/search/"
    pypi_project_url: str = "https://pypi.org/project/"
    pypi_json_url: str = "https://pypi.org/pypi/"
    pypi_simple_index_url: str = "https://pypi.org/simple/"
    idlemode = 1 if "idlelib.run" in sys.modules else 0


config = Config()
config.project_count = project_count


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
            print(Fore.RED + Back.BLACK + Style.BRIGHT + f"{message}" + Style.RESET_ALL)


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


def _rename_project_dir(old_name: str, new_name: str) -> None:
    """Utility script to rename a directory.

    The object being to rename a 'template' directory for the purpose of creating a
    minimalist package for upload to PyPI.

    Args:
        old_name:       source name.
        new_name:       dst name.

    Raises:
        FileNotFoundError
    """
    old_directory_path = Path(old_name)
    new_directory_path = Path(new_name)
    logger.debug("renaming project directory from %s to %s", old_name, new_name)
    try:
        old_directory_path.rename(new_directory_path)
    except FileNotFoundError:
        logger.error("directory %s cannot be found:", old_directory_path)
        raise FileNotFoundError


def _create_setup(new_project_name: str) -> None:
    """Utility script to create a setup.py file.

    The object being to create a setup.py file from a 'template' file for the purpose of
    creating a minimalist package for upload to PyPI.

    Args:
        new_project_name:       name used to render the template.
    """
    template = Template(setup_text)
    content = template.render(
        PROJECT_NAME=new_project_name,
        PACKAGE_VERSION=config.package_version,
    )
    setup_file = project_path.joinpath("setup.py")
    with open(setup_file, mode="w", encoding="utf-8") as message:
        logger.debug("creating new setup.py with the following: \n %s", content)
        message.write(content)


def _delete_director(items_to_delete: list[Path]) -> None:
    """Utility function to delete files and directories.

    Args:
        items_to_delete:    A list of Path like objects to delete.
    """
    for item in items_to_delete:
        if not item.exists():
            logger.debug("trying to delete %s but it does not exist", item)
            continue
        if item.is_dir():
            logger.debug("Deleting Directory: %s", item)
            shutil.rmtree(item, ignore_errors=True)
        else:
            logger.debug("Deleting File: %s", item)
            Path.unlink(item, missing_ok=True)


def _run_command(
    *arguments: str,
    shell: bool = True,
    capture_output: bool = False,
    text: bool = True,
    working_dir: Union[Path, str, None] = None,
    project: Union[None, str] = None,
) -> None:
    """Utility designed to execute a command line utility.

    Args:
        arguments:  Comma separated strings- "utility", "arg1", "arg2", etc.
        shell:      command executed by the shell or directly by the operating system.
        cwd:        specifies the current working directory to use when starting
                    the subprocess.
                    e.g. "/home/user/mydir"
        project:    the name of the project currently being tested
    """
    working_dir = os.getcwd() if working_dir is None else working_dir
    try:
        process = subprocess.Popen(
            arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=shell,
            text=True,
            cwd=working_dir,
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            logger.error("Error running command: %s", arguments)
            logger.error("stderr: %s", stderr)
            if project is not None:
                _cleanup(project)
            return
        logger.debug("%s", stdout)
        return stdout
    except Exception as e:
        logger.error("Exception running command: %s", arguments)
        logger.error(e)
        if project is not None:
            _cleanup(project)
        return


def _ping_project(project_name: str) -> bool:
    """Determines if the URL to the project exists on PyPI.

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
        project_ping = requests.get(url_project, timeout=10)
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
        project_json_raw = requests.get(url_json, timeout=10)
    except requests.RequestException as e:
        logger.error("An error occurred: %s", e)
        raise SystemExit("An error occurred with an HTTP request")
    if project_json_raw.status_code == 200:
        project_json = json.loads(project_json_raw.content)
        result = "".join(
            [
                project_json["info"]["author"],
                "\n",
                project_json["info"]["author_email"],
                "\n",
                project_json["info"]["version"],
                "\n",
                project_json["info"]["summary"],
            ]
        )
        return result
    logger.debug("No response from JSON URL")
    return ""


def _build_dist() -> None:
    """Builds the sdist and wheel of the minimalist project to upload to PyPI."""
    logger.debug("Building the distribution... ")
    builder = build.ProjectBuilder(project_path)
    builder.build("wheel", project_path / "dist")
    builder.build("sdist", project_path / "dist")


def _upload_dist(project_name: str) -> None:
    """Builds the twine command line to upload the minimalist project to PyPI.

    Args:
        project_name:   the name of the project currently under test.

    Notes:
        twine expects a filesystem path not Path object so use os.fspath()
    """
    logger.debug("Uploading the distribution... ")
    dir_path = os.fspath(project_path / "dist" / "*")
    pypirc_path = os.fspath(config.pypirc)  # type: ignore
    _run_command(
        sys.executable,
        "-m",
        "twine",
        "upload",
        "--config-file",
        pypirc_path,
        dir_path,
        project=project_name,
    )


def _cleanup(project_name: str) -> None:
    """Builds a manifest of artifacts to delete into a list of Path objects.

    Args:
        project_name:   the name of the project currently under test.
    """
    if config.no_cleanup is True:
        return
    _rename_project_dir(
        project_path.joinpath(project_name),
        project_path.joinpath(config.original_project_name),
    )
    build_artifacts = [
        project_path / "build",
        project_path / "dist",
        project_path / "".join([project_name, ".egg-info"]),
        project_path / "setup.py",
    ]
    logger.debug("cleaning build artifacts %s", build_artifacts)
    _delete_director(build_artifacts)


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
    progress_bar = tqdm(total=config.project_count)
    pypi_index = project_path / "pypi_index"
    pypi_count = project_path / "project_count.pickle"
    if pypi_index.exists():
        Path.unlink(pypi_index, missing_ok=True)
    try:
        index_object_raw = requests.get(config.pypi_simple_index_url, timeout=10)
    except requests.RequestException as e:
        logger.error("An error occurred: %s", e)
        raise SystemExit("An error occurred with an HTTP request")
    with pypi_index.open(mode="a") as file:
        for line in index_object_raw.iter_lines():
            line = str(line)
            project_text = re.search(pattern, line)
            if project_text is not None:
                new_count += 1
                progress_bar.update(1)
                project = "".join([project_text.group(1), " \n"])
                file.write(project)
    progress_bar.close()
    with open(pypi_count, "wb") as f:
        pickle.dump(new_count, f)


def _pypi_search_index(project_name: str) -> bool:
    """Open the generated index file and search for the project name.

    Args:
        project_name:   the name of the project currently under test.

    Returns:
        True:           A match was found.
        False:          A match was not found.
    """
    pypi_index = project_path / "pypi_index"
    if not pypi_index.exists():
        _generate_pypi_index()
    with pypi_index.open(mode="r") as file:
        projects = file.read()
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
        search_project:   the name of the project currently under test.

    Returns:
        match:          A list of projects matching name comprising:
                            [project_name, version, released, description]
        others:         A list of projects not matching but PyPI thinks are relevant.
                            [project_name, version, released, description]
        others_total:   A str representation of total projects found (minus matches).
    """
    pattern = re.compile(r">([\d,+]*?)<")
    s = requests.Session()
    projects_raw, match, others = [], [], []
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
    if not file_path.exists():
        raise SystemExit(f"The file {file} does not exist")
    with file_path.open(mode="r") as f:
        file_contents = f.read()
        projects = file_contents.split()
        return list(set(projects))


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
    title = f"Results from pynamer PyPI utility\n"
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
    with file_path.open(mode="w") as f:
        f.write(title)
        f.write(header)
        f.write(projects_results)


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


def main():
    parser = argparse.ArgumentParser(
        prog="pynamer",
        description="Determine if project name is available on pypi with the "
        "option to 'register' it for future use if available",
    )
    parser.add_argument(
        "projects",
        nargs="*",
        default="None",
        help="Optional - one or more project names",
    )
    parser.add_argument(
        "-r",
        "--register",
        action="store_true",
        help="Register the name on PyPi if the name is available",
    )
    parser.add_argument(
        "-d",
        "--dryrun",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-f",
        "--file",
        default="None",
        type=str,
        help="File containing a list of projects to analyze",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="None",
        type=str,
        help="File to output the results to",
    )
    parser.add_argument(
        "-n",
        "--nocleanup",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="output additional information",
    )
    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="Generate a new PyPI simple index",
    )

    args = parser.parse_args()
    logger.debug(" args: %s", args)

    if args.generate is True:
        _generate_pypi_index()

    if args.projects == "None" and args.file == "None":
        parser.print_help()
        raise SystemExit("No projects to analyse")

    project_list = []
    test_results = []
    aggregated_result = {}
    _find_pypirc_file()
    if args.nocleanup is True:
        config.no_cleanup = True

    # Gather the projects into one list
    if args.projects != "None":
        logger.debug("adding project names from command line %s", args.projects)
        project_list.extend(list(set(args.projects)))
        logger.debug("project_list = %s", project_list)
    if args.file != "None":
        logger.debug("adding project names from file %s", args.file)
        project_list.extend(_process_input_file(args.file))
        logger.debug("project_list = %s", project_list)
    project_list.sort()

    # Main loop
    for new_project in project_list:
        test_table = Table(title=f"Test Results for {new_project}", show_lines=True)
        test_table.add_column("No.", style="bold yellow")
        test_table.add_column("Test", style="bold cyan")
        test_table.add_column("Result")
        test_table.add_column("Details", style="bold cyan")

        match_table = Table(title=f"PyPI Search: Exact Match {new_project}")
        match_table.add_column("Package", style="bold yellow")
        match_table.add_column("Version", style="bold green")
        match_table.add_column("Released", style="bold yellow")
        match_table.add_column("Description", style="bold cyan")

        others_table = Table(
            title="Other Close Matches or Related Projects (from page 1)"
        )
        others_table.add_column("Package", style="bold yellow")
        others_table.add_column("Version", style="bold green")
        others_table.add_column("Released", style="bold yellow")
        others_table.add_column("Description", style="bold cyan")

        # perform the tests
        # Test 1
        if _ping_project(new_project):
            test_results.append(1)
            json_data = _ping_json(new_project)
            test_table.add_row(
                "1", "Basic http get to project URL", "[red]FOUND[/red]", json_data
            )
        else:
            test_results.append(0)
            test_table.add_row(
                "1", "Basic http get to project URL", "[green]NOT FOUND[/green]", ""
            )

        # Test 2
        if _pypi_search_index(new_project):
            test_results.append(1)
            test_table.add_row(
                "2",
                "Check PyPI simple index",
                "[red]FOUND[/red]",
                f"Searched {project_count} projects",
            )
        else:
            test_results.append(0)
            test_table.add_row(
                "2",
                "Check PyPI simple index",
                "[green]NOT FOUND[/green]",
                f"Searched {project_count} projects",
            )

        # Test 3
        match, others, others_total = _pypi_search(new_project)
        if match:
            test_results.append(1)
            test_table.add_row(
                "3",
                "Check PyPI search",
                "[red]FOUND[/red]",
                f"Exact match found: {len(match)}, Others found: {others_total}",
            )
            for items in match:
                match_table.add_row(items[0], items[1], items[2], items[3])
        else:
            test_results.append(0)
            test_table.add_row(
                "3",
                "Check PyPI search",
                "[green]NOT FOUND[/green]",
                f"Exact match found: 0, Others found: {others_total}",
            )

        # Create Verbose Table
        if others:
            for items in others:
                others_table.add_row(items[0], items[1], items[2], items[3])

        # Display the Tables
        console = Console()
        console.print(test_table)
        if match:
            console.print(match_table)
        if args.verbose and others:
            console.print(others_table)
        _final_analysis(test_results)

        # build and upload
        if (
            test_results == [0, 0, 0]
            and args.register is True
            and config.pypirc is not None
        ):
            _rename_project_dir(
                project_path.joinpath(config.original_project_name),
                project_path.joinpath(new_project),
            )
            _create_setup(new_project)
            _build_dist()
            if args.dryrun is False:
                _upload_dist(new_project)
            else:
                _feedback("Dryrun .... bypassing upload to PyPI..", "warning")
            _cleanup(new_project)
        elif config.pypirc is None:
            _feedback(
                ".pypirc file cannot be located ... wont attempt to 'register'",
                "error",
            )
        elif sum(test_results) > 0 and args.register is True:
            _feedback("Project already exists ... wont attempt to 'register'", "error")

        aggregated_result[new_project] = test_results.copy()
        test_results.clear()

    if args.output != "None":
        _write_output_file(args.output, aggregated_result)


if __name__ == "__main__":
    SystemExit(main())
