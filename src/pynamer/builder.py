#!/usr/bin/env python3

# Core Library modules
import os
import pickle
import re
import shutil
import subprocess
import sys
from importlib.resources import as_file
from pathlib import Path
from typing import Any, Union

# Third party modules
import build
from colorama import Back, Fore, Style
from jinja2 import Template

# Local modules
from . import (
    logger,
    meta,
    meta_file_trv,
    project_path,
    setup_base_file_trv,
    setup_file_py_trv,
    setup_file_trv,
    setup_text,
)
from .config import config
from .utils import _feedback


def _create_setup(new_project_name: str, new_meta: bool = False) -> None:
    """Utility script to create a setup.py file.

    The object being to create a setup.py file from a 'template' file for the purpose of
    creating a minimalist package for upload to PyPI.

    Args:
        new_project_name:       name used to render the template.
    """
    # setup_file_py_trv = project_path / "setup.py"

    author = meta["author"] if meta else ""
    email = meta["email"] if meta else ""
    description = meta["description"] if meta else config.description
    version = meta["version"] if meta else config.package_version

    _email_pattern = (
        r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:"
        r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    )

    if "AUTHOR" in setup_text or "EMAIL" in setup_text or not meta or new_meta:
        try:
            while True:
                author = (
                    input(
                        Fore.YELLOW
                        + Back.BLACK
                        + Style.BRIGHT
                        + f"please enter your author name ({author}): "
                        + Style.RESET_ALL
                    )
                    or author
                )
                if author != "":
                    break
        except KeyboardInterrupt:  # pragma: no cover
            _feedback("...bye!", "warning")
            raise SystemExit()

        try:
            while True:
                email = (
                    input(
                        Fore.YELLOW
                        + Back.BLACK
                        + Style.BRIGHT
                        + f"please enter your email address ({email}): "
                        + Style.RESET_ALL
                    )
                    or email
                )
                if re.search(_email_pattern, email):
                    break
                else:
                    print(
                        Fore.YELLOW
                        + Back.BLACK
                        + Style.BRIGHT
                        + "does not appear to be a valid email address"
                        + Style.RESET_ALL
                    )  # pragma: no cover
        except KeyboardInterrupt:  # pragma: no cover
            _feedback("...bye!", "warning")
            raise SystemExit()

        try:
            while True:
                version = (
                    input(
                        Fore.YELLOW
                        + Back.BLACK
                        + Style.BRIGHT
                        + f"version number: ({version}): "
                        + Style.RESET_ALL
                    )
                    or version
                )
                if version != "":
                    break
        except KeyboardInterrupt:  # pragma: no cover
            raise SystemExit("Bye!")

        try:
            while True:
                description = (
                    input(
                        Fore.YELLOW
                        + Back.BLACK
                        + Style.BRIGHT
                        + f"description: ({description}): "
                        + Style.RESET_ALL
                    )
                    or description
                )
                if description != "":
                    break
        except KeyboardInterrupt:  # pragma: no cover
            raise SystemExit("Bye!")

        with as_file(setup_file_trv) as setup_file:
            if setup_file.exists():
                setup_file.unlink(missing_ok=True)

        setup_text_base = setup_base_file_trv.read_text(encoding="utf-8")
        template = Template(setup_text_base)
        content = template.render(
            PROJECT_NAME="{{ PROJECT_NAME }}",
            PACKAGE_VERSION=version,
            DESCRIPTION=description,
            AUTHOR=author,
            EMAIL=email,
        )
        with setup_file_trv.open("w", encoding="utf-8") as f:
            f.write(content)

    meta_save = {
        "author": author,
        "email": email,
        "description": description,
        "version": version,
    }
    with meta_file_trv.open("wb") as f:
        pickle.dump(meta_save, f)

    setup_text_file = setup_file_trv.read_text(encoding="utf-8")
    template = Template(setup_text_file)
    content = template.render(PROJECT_NAME=new_project_name)

    with setup_file_py_trv.open("w", encoding="utf-8") as message:
        logger.debug("creating new setup.py with the following: \n %s", content)
        message.write(content)


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


def _delete_director(items_to_delete: Any) -> None:
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


def _cleanup(project_name: str) -> None:
    """Builds a manifest of artifacts to delete into a list of Path objects.

    Args:
        project_name:   the name of the project currently under test.
    """
    if config.no_cleanup is True:  # pragma: no cover
        return
    _rename_project_dir(
        str(project_path.joinpath(project_name)),
        str(project_path.joinpath(config.original_project_name)),
    )
    build_artifacts = [
        project_path / "build",
        project_path / "dist",
        project_path / "".join([project_name, ".egg-info"]),
        project_path / "setup.py",
    ]
    logger.debug("cleaning build artifacts %s", build_artifacts)
    _delete_director(build_artifacts)


def _run_command(
    *arguments: str,
    shell: bool = True,
    working_dir: Union[Path, str, None] = None,
    project: Union[None, str] = None,
) -> None:  # pragma: no cover
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
        return
    except Exception as e:
        logger.error("Exception running command: %s", arguments)
        logger.error(e)
        if project is not None:
            _cleanup(project)
        return


def _upload_dist(project_name: str) -> None:
    """Builds the twine command line to upload the minimalist project to PyPI.

    Args:
        project_name:   the name of the project currently under test.

    Notes:
        twine expects a filesystem path not Path object so use os.fspath()
    """
    logger.debug("Uploading the distribution... ")

    project_build = str(project_path / "dist" / "*")
    dir_path = os.fspath(project_build)
    pypirc_path = os.fspath(str(config.pypirc))
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


def _build_dist() -> None:
    """Builds the sdist and wheel of the minimalist project to upload to PyPI."""
    logger.debug("Building the distribution... ")
    builder = build.ProjectBuilder(project_path)
    builder.build("wheel", project_path / "dist")
    builder.build("sdist", project_path / "dist")
