
import requests
from dateutil.parser import isoparse


class Config:
    """Configuration class"""

    pypi_search_url: str = "https://pypi.org/search/"
    pypi_project_url: str = "https://pypi.org/project/"
    pypi_json_url: str = "https://pypi.org/pypi/"
    pypi_simple_index_url: str = "https://pypi.org/simple/"
    github_api_url: str = "https://api.github.com/repos/"
    github_base_url: str = "https://github.com/"


config = Config()


def github_meta(url: str) -> str:
    """Finds GitHub statistics given a GitHub Homepage URL.

    Args:
        url:    GitHub homepage URL.

    Returns:
        str:    a string containing all the pertinent statistics:
    """
    return_text = "\n\nGitHub Stats\n------------\n"
    repo_api_url = "".join(
        [config.github_api_url, url.replace(r"https://github.com/", "")]
    )
    try:
        json_raw = requests.get(repo_api_url, timeout=5)
    except requests.RequestException:
        return "".join([return_text, "GitHub can not be contacted"])

    if json_raw.status_code == 200:
        repo_json = json_raw.json()

        license_name = (
            repo_json["license"]["name"] if repo_json["license"] is not None else "None"
        )

        return "".join(
            [
                return_text,
                f"stars:    {repo_json['stargazers_count']}",
                "\n",
                f"forks:    {repo_json['forks']}",
                "\n",
                f"issues:   {repo_json['open_issues']}",
                "\n",
                f"license:  {license_name}",
                "\n",
                f"watching: {repo_json['subscribers_count']}",
                "\n",
                f"created:  {isoparse(repo_json['created_at']).date()}",
                "\n",
                f"updated:  {isoparse(repo_json['updated_at']).date()}",
            ]
        )
    if json_raw.status_code == 404:
        return "".join(
            [
                return_text,
                "JSON API Does not exist.\n"
                "This usually indicates a very old repository.",
            ]
        )
    return ""


project = "https://github.com/psf/black"

stats = github_meta(project)

print(stats)
