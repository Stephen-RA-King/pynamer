#!/usr/bin/env python3

# Core Library modules
import argparse
import sys
import webbrowser
from pathlib import Path
from typing import Any, Union

# Third party modules
from rich.console import Console
from rich.table import Table

# Local modules
from . import logger, project_count, project_path
from .builder import (
    _build_dist,
    _cleanup,
    _create_setup,
    _rename_project_dir,
    _upload_dist,
)
from .config import config
from .utils import (
    _check_version,
    _feedback,
    _find_pypirc_file,
    _generate_pypi_index,
)
from .validators import (
    _is_valid_package_name,
    _ping_json,
    _ping_project,
    _pypi_search,
    _pypi_search_index,
)


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


def _parse_args(args: list) -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    """Function to return the ArgumentParser object created from all the args.

    Args:
        args:   A list of arguments from the commandline
                e.g. ['pynball', '-v', '-g']
    """
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
        help="register the name on PyPi if the name is available",
    )
    parser.add_argument(
        "-d",
        "--dryrun",
        action="store_true",
        help=argparse.SUPPRESS,
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
        help="display information about similar projects",
    )
    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="generate a new PyPI index file",
    )
    parser.add_argument(
        "-m",
        "--meta",
        action="store_true",
        help="input new meta data when registering (Author and email address)",
    )

    parser.add_argument(
        "-w",
        "--webbrowser",
        action="store_true",
        help="open the project on PyPI in a webbrowser",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="display version number",
    )
    parser.add_argument(
        "-f",
        "--file",
        default="None",
        type=str,
        help="file containing a list of projects to analyze",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="None",
        type=str,
        help="file to store the test results",
    )
    return parser.parse_args(args), parser


def main() -> None:  # pragma: no cover, type: ignore
    args, parser = _parse_args(sys.argv[1:])
    logger.debug(" args: %s", args)

    if args.generate:
        _generate_pypi_index()

    if args.version:
        version, message, result = _check_version()  # type: ignore
        if result:
            _feedback(f"{version} : {message}", "nominal")
        else:
            _feedback(f"{version} : {message}", "warning")

    if args.projects == "None" and args.file == "None" and args.register:
        _feedback("You need to specify a project name to register it", "error")
        raise SystemExit()

    if args.projects == "None" and args.file == "None" and args.meta:
        _feedback(
            "You can only update the meta data during the registration process", "error"
        )
        raise SystemExit()

    if (
        args.projects == "None"
        and args.file == "None"
        and args.version is False
        and args.generate is False
    ):
        parser.print_help()
        raise SystemExit()

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
        if not _is_valid_package_name(new_project):
            _feedback(f"{new_project} is not a valid package name", "error")
            continue

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
            and len(project_list) == 1
        ):
            _create_setup(new_project, new_meta=args.meta)
            _rename_project_dir(
                str(project_path.joinpath(config.original_project_name)),
                str(project_path.joinpath(new_project)),
            )
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

    if args.register and len(project_list) > 1:
        _feedback(
            f"You can only use 'register' for one project at a time. "
            f"You have specified {len(project_list)} projects",
            "warning",
        )

    if args.webbrowser:
        if len(project_list) == 1:
            url_project = "".join([config.pypi_project_url, project_list[0], "/"])
            webbrowser.open(url_project)
        else:
            _feedback(
                f"You must choose one project to open the webbrowser. "
                f"You have chosen {len(project_list)} projects",
                "warning",
            )


if __name__ == "__main__":
    SystemExit(main())  # type: ignore
