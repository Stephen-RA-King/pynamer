# Core Library modules
import pickle
from pathlib import Path

# Third party modules
import requests

BASE_DIR = Path(__file__).parents[1]

pypi_search_url = "https://pypi.org/search/"
pypi_project_url = "https://pypi.org/project/"
pypi_json_url = "https://pypi.org/pypi/"
pypi_simple_index_url = "https://pypi.org/simple/"


def ping_project(name):
    ping_file_name = (
        BASE_DIR / "resources" / "".join(["requests_get_ping_", name, ".pickle"])
    )
    url = "".join([pypi_project_url, name, "/"])
    r = requests.get(url, timeout=5)
    with open(ping_file_name, "wb") as f:
        pickle.dump(r, f)


def json_project(name):
    json_file_name = (
        BASE_DIR / "resources" / "".join(["requests_get_json_", name, ".pickle"])
    )
    url = "".join([pypi_json_url, name, "/json"])
    r = requests.get(url, timeout=5)
    with open(json_file_name, "wb") as f:
        pickle.dump(r, f)


def search(name):
    search_file_name = (
        BASE_DIR / "resources" / "".join(["requests_get_search_", name, ".pickle"])
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
    index_file_name = BASE_DIR / "resources" / "simple_index.pickle"
    response = requests.Response()
    response.status_code = 200
    response.headers = {"Content-Type": "application/json"}
    response._content = small_content
    with open(index_file_name, "wb") as f:
        pickle.dump(response, f)
