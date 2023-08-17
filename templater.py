#!/usr/bin/env python3
# Core Library modules
import re
from pathlib import Path
from typing import Any, Optional

# Third party modules
import requests
from bs4 import BeautifulSoup
from requests import RequestException

env_file = "".join([Path(__file__).stem, ".env"])


def write_to_env_file(key: str, value: str) -> None:  # type: ignore
    entry = "".join([key, "=", value, "\n"])
    with open(env_file, mode="a") as file:
        file.write(entry)


def get_value1() -> None:
    text: str = ""
    try:
        html: Any = requests.get("https://pypi.org/", timeout=5)
    except RequestException as e:
        print(f"There was a problem with the request: {e}")
        html = ""
    if html != "":
        soup = BeautifulSoup(html.content, "html.parser")
        target_div = soup.find("div", class_="statistics-bar")
        pattern = r"\d{1,3}(?:,\d{3})*"
        if target_div:
            p_elements = target_div.find_all("p")  # type: ignore
            for p in p_elements:
                text = p.text
                if "projects" in text:
                    break

        match: Optional[re.Match] = re.search(pattern, text)
        if match is not None:
            matched_text: str = match.group()
            write_to_env_file("PROJECT_COUNT_HYPHEN", matched_text)
            matched_text = matched_text.replace(",", "")
            write_to_env_file("PROJECT_COUNT", matched_text)


def main():  # type: ignore
    get_value1()


if __name__ == "__main__":
    SystemExit(main())
