#!/usr/bin/env python3

# Core Library modules
import sys
import webbrowser

# Third party modules
from rich.console import Console
from rich.table import Table

# Local modules
from . import logger, project_count, project_path
from .builder import (
    build_dist,
    cleanup,
    create_setup,
    rename_project_dir,
    upload_dist,
)
from .cli import _parse_args
from .config import config
from .utils import (
    check_version,
    feedback,
    find_pypirc_file,
    generate_pypi_index,
    process_input_file,
    write_output_file,
)
from .validators import (
    final_analysis,
    is_valid_package_name,
    ping_json,
    ping_project,
    pypi_search,
    pypi_search_index,
)


def main() -> None:  # pragma: no cover, type: ignore
    args, parser = _parse_args(sys.argv[1:])
    logger.debug(" args: %s", args)

    if args.generate:
        generate_pypi_index()

    if args.version:
        check_version()

    if args.projects == "None" and args.f == "None" and args.register:
        feedback("You need to specify a project name to register it", "error")
        raise SystemExit()

    if args.projects == "None" and args.f == "None" and args.meta:
        feedback(
            "You can only update the meta data during the registration process", "error"
        )
        raise SystemExit()

    if (
        args.projects == "None"
        and args.f == "None"
        and args.version is False
        and args.generate is False
    ):
        parser.print_help()
        raise SystemExit()

    project_list = []
    test_results = []
    aggregated_result = {}
    find_pypirc_file()
    if args.nocleanup is True:
        config.no_cleanup = True

    # Gather the projects into one list
    if args.projects != "None":
        logger.debug("adding project names from command line %s", args.projects)
        project_list.extend(list(set(args.projects)))
        logger.debug("project_list = %s", project_list)
    if args.f != "None":
        logger.debug("adding project names from file %s", args.f)
        project_list.extend(process_input_file(args.f))
        logger.debug("project_list = %s", project_list)
    project_list.sort()

    # Main loop
    for new_project in project_list:
        if not is_valid_package_name(new_project):
            feedback(f"{new_project} is not a valid package name", "error")
            feedback("refer to PEP508 & PEP423 for more details", "warning")
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
        if ping_project(new_project):
            test_results.append(1)
            if args.stats is True:
                json_data = ping_json(new_project, stats=True)
            else:
                json_data = ping_json(new_project)
            test_table.add_row(
                "1", "Check PyPI project URL", "[red]FOUND[/red]", json_data
            )
        else:
            test_results.append(0)
            test_table.add_row(
                "1", "Check PyPI project URL", "[green]NOT FOUND[/green]", ""
            )

        # Test 2
        if pypi_search_index(new_project):
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
        match, others, others_total = pypi_search(new_project)
        if match:
            test_results.append(1)
            test_table.add_row(
                "3",
                "Check PyPI search API",
                "[red]FOUND[/red]",
                f"Exact match found: {len(match)}, Others found: {others_total}",
            )
            for items in match:
                match_table.add_row(items[0], items[1], items[2], items[3])
        else:
            test_results.append(0)
            test_table.add_row(
                "3",
                "Check PyPI search API",
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
        final_analysis(test_results)

        # build and upload
        if (
            test_results == [0, 0, 0]
            and args.register is True
            and config.pypirc is not None
            and len(project_list) == 1
        ):
            create_setup(new_project, new_meta=args.meta)
            rename_project_dir(
                str(project_path.joinpath(config.original_project_name)),
                str(project_path.joinpath(new_project)),
            )
            build_dist()
            if args.dryrun is False:
                upload_dist(new_project)
            else:
                feedback("Dryrun .... bypassing upload to PyPI..", "warning")
            cleanup(new_project)
        elif args.register is True and config.pypirc is None:
            feedback(
                ".pypirc file cannot be located ... wont attempt to 'register'",
                "error",
            )
        elif sum(test_results) > 0 and args.register is True:
            feedback("Project already exists ... wont attempt to 'register'", "error")

        aggregated_result[new_project] = test_results.copy()
        test_results.clear()

    if args.o != "None":
        write_output_file(args.o, aggregated_result)

    if args.register and len(project_list) > 1:
        feedback(
            f"You can only use 'register' for one project at a time. "
            f"You have specified {len(project_list)} projects",
            "warning",
        )

    if args.webbrowser:
        if len(project_list) == 1:
            url_project = "".join([config.pypi_project_url, project_list[0], "/"])
            webbrowser.open(url_project)
        else:
            feedback(
                f"You must choose one project to open the webbrowser. "
                f"You have chosen {len(project_list)} projects",
                "warning",
            )


if __name__ == "__main__":
    SystemExit(main())  # type: ignore
