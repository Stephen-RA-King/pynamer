#!/usr/bin/env python3

# Core Library modules
import argparse
import json
import logging.config
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Third party modules
import requests  # type: ignore
import yaml  # type: ignore
from jinja2 import Environment, FileSystemLoader

ROOT_DIR = Path.cwd()
ORIGINAL_PROJECT_NAME = "project_name"


try:
    with open("log_config.yaml") as log_config:
        logging.config.dictConfig(yaml.safe_load(log_config))
    logger = logging.getLogger("main")
except FileNotFoundError:
    raise SystemExit(
        "trying to configure logging but 'log_config.yaml' cannot be found"
    )


def rename_project_dir(old_name: str, new_name: str) -> None:
    old_directory_path = Path(old_name)
    new_directory_path = Path(new_name)
    logger.debug("renaming project directory from %s to %s", old_name, new_name)
    try:
        old_directory_path.rename(new_directory_path)
    except FileNotFoundError:
        logger.error("directory %s cannot be found:", old_directory_path)


def create_setup(new_project_name: str) -> None:
    environment = Environment(autoescape=True, loader=FileSystemLoader("."))
    template = environment.get_template("setup.txt")
    content = template.render(PROJECT_NAME=new_project_name)
    with open("setup.py", mode="w", encoding="utf-8") as message:
        logger.debug("creating new setup.py with the following: \n %s", content)
        message.write(content)


def delete_director(items_to_delete: list) -> None:
    """Utility function to delete files or directories"""
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


def run_command(*arguments: str, shell=False, working_dir=None, project=None) -> None:
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
            logger.error("Error running command: %s", args)
            logger.error("stderr: %s", stderr)
            cleanup(project)
            return
        logger.debug("%s", stdout)
        return
    except Exception as e:
        logger.error("Exception running command: %s", args)
        logger.error(e)
        cleanup(project)
        return


def ping_project(new_project_name: str) -> bool:
    url_project = "".join(["https://pypi.org/project/", new_project_name, "/"])
    logger.debug("attempting to get url %s", url_project)
    project_ping = requests.get(url_project, timeout=10)
    if project_ping.status_code == 200:
        logger.info("%s EXISTS", new_project_name)
        if args.output != "None":
            message = f"{new_project_name:20} is already registered"
            write_output_file(args.output, message)
        return True
    else:
        logger.info("%s DOES NOT EXIST", new_project_name)
        if args.output != "None":
            message = f"{new_project_name:20} is available"
            write_output_file(args.output, message)
        return False


def ping_json(new_project_name: str) -> bool:
    url_json = "".join(["https://pypi.org/pypi/", new_project_name, "/json"])
    logger.debug("attempting to get url %s", url_json)
    project_json_raw = requests.get(url_json, timeout=10)
    if project_json_raw.status_code == 200:
        project_json = json.loads(project_json_raw.content)
        author = project_json["info"]["author"]
        logger.info("Author: %s", author)
        logger.info("Author Email: %s", project_json["info"]["author_email"])
        logger.info("Summary: %s", project_json["info"]["summary"])
        logger.info("Latest Version: %s", project_json["info"]["version"])
        return True
    else:
        logger.info("No response from JSON URL")
        return False


def build_dist(project_name):
    logger.info("Building the distribution... ")
    run_command(
        sys.executable, "-m", "build", "--sdist", "--wheel", ".", project=project_name
    )


def upload_dist(project_name):
    logger.info("Uploading the distribution... ")
    run_command(
        sys.executable,
        "-m",
        "twine",
        "upload",
        "--config-file",
        ".pypirc",
        "dist/*",
        project=project_name,
    )
