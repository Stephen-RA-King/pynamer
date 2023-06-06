# Core Library modules
import json
import pickle
from pathlib import Path

# Third party modules
import requests
from dateutil.parser import isoparse

BASE_DIR = Path(__file__).parents[1]

pypi_search_url = "https://pypi.org/search/"
pypi_project_url = "https://pypi.org/project/"
pypi_json_url = "https://pypi.org/pypi/"
pypi_simple_index_url = "https://pypi.org/simple/"
github_api_url = "https://api.github.com/repos/"


def ping_project(name):
    ping_file_name = (
        BASE_DIR / "tests" / "resources" / "".join(["requests_get_ping_", name, ".pkl"])
    )
    url = "".join([pypi_project_url, name, "/"])
    r = requests.get(url, timeout=5)
    with open(ping_file_name, "wb") as f:
        pickle.dump(r, f)


def json_save(name):
    json_file_name = (
        BASE_DIR
        / "tests"
        / "resources"
        / "".join(["requests_get_json_", name, ".pickle"])
    )
    url = "".join([pypi_json_url, name, "/json"])
    r = requests.get(url, timeout=5)
    # j = r.content.decode('utf-8')
    with open(json_file_name, "wb") as f:
        pickle.dump(r, f)


def json_open(name):
    json_file_name = (
        BASE_DIR
        / "tests"
        / "resources"
        / "".join(["requests_get_json_", name, ".pickle"])
    )
    with open(json_file_name, "rb") as f:
        response = pickle.load(f)
    print(type(response))
    print(response.status_code)
    project_json = json.loads(response.content)
    print(project_json["info"]["author"])
    print(project_json["info"]["author"])
    print(project_json["info"]["author"])
    print(project_json["info"]["author"])
    print(project_json["info"]["author"])


def search(name):
    search_file_name = (
        BASE_DIR
        / "tests"
        / "resources"
        / "".join(["requests_get_search_", name, ".pickle"])
    )
    params = {"q": {name}, "page": 1}
    r = requests.get(pypi_search_url, params=params, timeout=5)
    with open(search_file_name, "wb") as f:
        pickle.dump(r, f)


small_content = b"""
<html>
  <head>
    <meta name="pypi:repository-version" content="1.1">
    <title>Simple index</title>
  </head>
  <body>
    <a href="/simple/pynavigator/">pynavigator</a>
    <a href="/simple/pynavio/">pynavio</a>
    <a href="/simple/pynavis/">pyNAVIS</a>
    <a href="/simple/pynavmesh/">pynavmesh</a>
    <a href="/simple/pynavt/">pynavt</a>
    <a href="/simple/pynb/">pynb</a>
    <a href="/simple/pynb2docker/">pynb2docker</a>
    <a href="/simple/pynba/">pynba</a>
    <a href="/simple/pynbaapi/">pynbaapi</a>
    <a href="/simple/pynball/">pynball</a>
    <a href="/simple/py-nba-stats/">py-nba-stats</a>
    <a href="/simple/pynbcache/">pynbcache</a>
    <a href="/simple/pynb-dag-runner/">pynb-dag-runner</a>
    <a href="/simple/pynb-dag-runner-snapshot/">pynb-dag-runner-snapshot</a>
    <a href="/simple/pynb-dag-runner-webui/">pynb-dag-runner-webui</a>
    </body>
</html>"""


def manual_simple_index():
    index_file_name = BASE_DIR / "tests" / "resources" / "simple_index.pickle"
    response = requests.Response()
    response.status_code = 200
    response.headers = {"Content-Type": "application/json"}
    response._content = small_content
    with open(index_file_name, "wb") as f:
        pickle.dump(response, f)


def get_github_meta(url):
    print(url)
    return_text = "GitHub Stats\n------------\n"
    if "github.io in" in url:
        for item in (".github.io", "https://"):
            url = url.replace(item, "")
        repo_api_url = "".join([github_api_url, url])
    else:
        repo_api_url = "".join(
            [github_api_url, url.replace(r"https://github.com/", "")]
        )
    print(repo_api_url)
    try:
        json_raw = requests.get(repo_api_url, timeout=5)
    except requests.RequestException as e:
        return "".join([return_text, "GitHub can not be contacted."])
    if json_raw.status_code == 200:
        repo_json = json_raw.json()
        return "".join(
            [
                return_text,
                f"stars: {repo_json['stargazers_count']}",
                "\n",
                f"forks: {repo_json['forks']}",
                "\n",
                f"license: {repo_json['license']['name']}",
                "\n",
                f"watching: {repo_json['subscribers_count']}",
                "\n",
                f"created: {isoparse(repo_json['created_at']).date()}",
                "\n",
                f"updated: {isoparse(repo_json['updated_at']).date()}",
            ]
        )
    elif json_raw.status_code == 404:
        return "".join([return_text, "GitHub reports repository does not exist."])


def save_github_meta(url, project_name):
    json_file_name = (
        BASE_DIR
        / "tests"
        / "resources"
        / "".join(["requests_get_github_json_", project_name, ".pickle"])
    )
    if "github.io in" in url:
        for item in (".github.io", "https://"):
            url = url.replace(item, "")
        repo_api_url = "".join([github_api_url, url])
    else:
        repo_api_url = "".join(
            [github_api_url, url.replace(r"https://github.com/", "")]
        )
    request_response = requests.get(repo_api_url, timeout=5)
    with open(json_file_name, "wb") as f:
        pickle.dump(request_response, f)


# json_save("requests")
# print(github_meta("https://github.com/pycqa/isort"))
# json_open("pynamer")
save_github_meta("https://github.com/psf/black", "black")
