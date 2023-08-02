#!/usr/bin/env python3
# Core Library modules
import re
from pathlib import Path

# Third party modules
import requests
from bs4 import BeautifulSoup
from requests import RequestException

env_file = "".join([Path(__file__).stem, ".env"])


def write_to_env_file(key, value):
    entry = "".join([key, "=", value, "\n"])
    with open(env_file, mode="a") as file:
        file.write(entry)


def get_value1():
    html, text = "", ""
    try:
        html = requests.get("https://pypi.org/", timeout=5)
    except RequestException as e:
        print(f"There was a problem with the request: {e}")
    soup = BeautifulSoup(html.content, "html.parser")
    target_div = soup.find("div", class_="statistics-bar")
    pattern = r"\d{1,3}(?:,\d{3})*"
    if target_div:
        p_elements = target_div.find_all("p")
        for p in p_elements:
            text = p.text
            if "projects" in text:
                break
    match = re.search(pattern, text).group()
    write_to_env_file("PROJECT_COUNT_HYPHEN", match)
    match = match.replace(",", "")
    write_to_env_file("PROJECT_COUNT", match)


def main():
    get_value1()


if __name__ == "__main__":
    SystemExit(main())
