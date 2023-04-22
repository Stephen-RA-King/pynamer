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
    with open("log_config.yaml") as f:
        logging.config.dictConfig(yaml.safe_load(f))
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


def run_command(*arguments, shell=False, working_dir=None, project=None):
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
