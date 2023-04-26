# pynamer

_**Utility to find an available package name on the PyPI repository and optionally 'register' it.**_

[![PyPI][pypi-image]][pypi-url]
[![Downloads][downloads-image]][downloads-url]
[![Status][status-image]][pypi-url]
[![Python Version][python-version-image]][pypi-url]
[![Format][format-image]][pypi-url]
[![tests][tests-image]][tests-url]
[![Codecov][codecov-image]][codecov-url]
[![pre-commit][pre-commit-image]][pre-commit-url]
[![pre-commit.ci status][pre-commit.ci-image]][pre-commit.ci-url]
[![CodeFactor][codefactor-image]][codefactor-url]
[![Codeclimate][codeclimate-image]][codeclimate-url]
[![CodeQl][codeql-image]][codeql-url]
[![readthedocs][readthedocs-image]][readthedocs-url]
[![Imports: isort][isort-image]][isort-url]
[![Code style: black][black-image]][black-url]
[![Checked with mypy][mypy-image]][mypy-url]
[![security: bandit][bandit-image]][bandit-url]
[![Commitizen friendly][commitizen-image]][commitizen-url]
[![Conventional Commits][conventional-commits-image]][conventional-commits-url]
[![DeepSource][deepsource-image]][deepsource-url]
[![license][license-image]][license-url]

As a pseudo replacement for pip search, pynamer will quickly ascertain if a project name is 'available' on PyPI.

![](assets/pynamer.png)

# Contents

-   [tl;dr](#TLDR)
-   [Introduction](#Introduction)
-   [Quick Start](#Quick-Start)
    -   [Prerequisites](#Prerequisites)
    -   [Installation](#Installation)
    -   [Basic Usage](#Basic-Usage-example)
-   [Documentation](#Documentation)
    -   [Read the Docs](https://pynamer.readthedocs.io/en/latest/)
    -   [Wiki](https://github.com/Stephen-RA-King/pynamer/wiki)

## Introduction

Some of you may have reached the point where you want to publish a package on the PyPI python repository.
The first step of which is to choose a unique name. Here lies the problem.

A recent look at the PyPI repository revealed there were over 449,007 projects, so many names have already been taken.

pip leaps to the rescue with its search utility... or does it?

```python
pip search zaphod
```

```commandline
ERROR: XMLRPC request failed [code: -32500]
RuntimeError: PyPI no longer supports 'pip search' (or XML-RPC search).
Please use https://pypi.org/search (via a browser) instead.
See https://warehouse.pypa.io/api-reference/xml-rpc.html#deprecated-methods for more information.
```

A quick search will show the internet replete with articles explaining the situation:

-   [The Register: Why Python's pip search isn't working](https://www.theregister.com/2021/05/25/pypi_search_error/)
-   [Pytyhon.org discussion: Pip search is still broken](https://discuss.python.org/t/pip-search-is-still-broken/18680)

OK so I go to the PyPI website and do a search for 'zaphod' as suggested by pip and 7 results are displayed none of which have the package name 'zaphod'

![](assets/pypi_zaphod.png)

Fantastic! I now think unbelievably that I have a unique name for a project that I can use.
So, I go ahead and code my new project, along with all the test files, documentation and meta data.
I diligently debug and commit and push to git and github so I have a history.

Finally the project is good enough to release and publish as an installable package on PyPI.

Here goes....

```commandline
python -m twine upload --config-file .pypirc dist/*
Uploading distributions to https://upload.pypi.org/legacy/
Uploading zaphod-0.0.0-py3-none-any.whl
100% ---------------------------------------- 3.8/3.8 kB • 00:00 • ?
WARNING  Error during upload. Retry with the --verbose option for more details.
ERROR    HTTPError: 403 Forbidden from https://upload.pypi.org/legacy/
         The user 'stephenking' isn't allowed to upload to project 'zaphod'. See https://pypi.org/help/#project-name for more information.
```

AARGH!

What just happened?

Yes unbelievably the project already exists and yes unbelievably PyPI's own search
did not find the project.

Enter Pynamer that does not rely on a single method of finding a PyPI package:

#### TLDR

Pynamer uses the following methods to ascertain whether a package already exists on PyPI:

-   A simple request to the project url on PyPI.
-   Uses the PyPI "simple" repository - a text-based listing of all the packages available on PyPI.
-   Uses PyPI's own search engine and scrapes the results.

Pynamer provides a way to optionally 'register' a name on PyPI by building a minimalistic package and uploading

## Quick Start

---

### Prerequisites

---

-   [x] Python >= 3.9.
-   [x] [**pipx**](https://pypa.github.io/pipx/)

The following are optional but required for 'registering' a project name on PyPI

-   [x] An account on PyPI (generate an API token).
-   [x] A [**.pypirc**](https://packaging.python.org/en/latest/specifications/pypirc/) file containing your PyPI API key

    or

-   [x] [Twine environment variables](https://twine.readthedocs.io/en/latest/#environment-variables)

Your .pypirc file should contain the following:

```file
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = your_API_key_here
```

### Installation

```sh
pipx install pynamer
```

### Basic Usage

```commandline
~ $ pynamer flake8

flake8 EXISTS
Author: Tarek Ziade
Author Email: tarek@ziade.org
Summary: the modular source code checker: pep8 pyflakes and co
Latest Version: 6.0.0
```

```commandline
~ $ pynamer zeedonk

zeedonk DOES NOT EXIST
```

# Usage

---

```commandline
pynamer --help
usage: pynamer [-h] [-r] [-d] [-f FILE] [-o OUTPUT] [-a] [projects ...]

Determine if project name is available on pypi with the option to 'register' it for future use if available

positional arguments:
  projects              Optional - one or more project names

optional arguments:
  -h, --help            show this help message and exit
  -r, --register        Register the name on PyPi if the name is available
  -d, --dryrun          Perform all tests but without uploading a dist to PyPI
  -f FILE, --file FILE  File containing a list of projects to analyze
  -o OUTPUT, --output OUTPUT
                        File to output the results to
  -a, --alltests        Perform all tests
```

## Documentation

---

[**Read the Docs**](https://pynamer.readthedocs.io/en/latest/)

-   [**Example Usage**](https://pynamer.readthedocs.io/en/latest/example.html)
-   [**Credits**](https://pynamer.readthedocs.io/en/latest/example.html)
-   [**Changelog**](https://pynamer.readthedocs.io/en/latest/changelog.html)
-   [**API Reference**](https://pynamer.readthedocs.io/en/latest/autoapi/index.html)

[**Wiki**](https://github.com/Stephen-RA-King/pynamer/wiki)

## Meta

---

[![](assets/linkedin.png)](https://www.linkedin.com/in/sr-king)
[![](assets/github.png)](https://github.com/Stephen-RA-King)
[![](assets/pypi.png)](https://pypi.org/project/pynamer)
[![](assets/www.png)](https://www.justpython.tech)
[![](assets/email.png)](mailto:sking.github@gmail.com)

Stephen R A King : [sking.github@gmail.com](sking.github@gmail.com)

Distributed under the MIT license. See [![][license-image]][license-url] for more information.

Created with Cookiecutter template: [**pydough**][pydough-url] version 1.2.2

<!-- Markdown link & img dfn's -->

[bandit-image]: https://img.shields.io/badge/security-bandit-yellow.svg
[bandit-url]: https://github.com/PyCQA/bandit
[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[pydough-url]: https://github.com/Stephen-RA-King/pydough
[codeclimate-image]: https://api.codeclimate.com/v1/badges/7fc352185512a1dab75d/maintainability
[codeclimate-url]: https://codeclimate.com/github/Stephen-RA-King/pynamer/maintainability
[codecov-image]: https://codecov.io/gh/Stephen-RA-King/pynamer/branch/main/graph/badge.svg
[codecov-url]: https://app.codecov.io/gh/Stephen-RA-King/pynamer
[codefactor-image]: https://www.codefactor.io/repository/github/Stephen-RA-King/pynamer/badge
[codefactor-url]: https://www.codefactor.io/repository/github/Stephen-RA-King/pynamer
[codeql-image]: https://github.com/Stephen-RA-King/pynamer/actions/workflows/github-code-scanning/codeql/badge.svg
[codeql-url]: https://github.com/Stephen-RA-King/pynamer/actions/workflows/github-code-scanning/codeql
[commitizen-image]: https://img.shields.io/badge/commitizen-friendly-brightgreen.svg
[commitizen-url]: http://commitizen.github.io/cz-cli/
[conventional-commits-image]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square
[conventional-commits-url]: https://conventionalcommits.org
[deepsource-image]: https://static.deepsource.io/deepsource-badge-light-mini.svg
[deepsource-url]: https://deepsource.io/gh/Stephen-RA-King/pynamer/?ref=repository-badge
[downloads-image]: https://static.pepy.tech/personalized-badge/pynamer?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads
[downloads-url]: https://pepy.tech/project/pynamer
[format-image]: https://img.shields.io/pypi/format/pynamer
[isort-image]: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
[isort-url]: https://github.com/pycqa/isort/
[lgtm-alerts-image]: https://img.shields.io/lgtm/alerts/g/Stephen-RA-King/pynamer.svg?logo=lgtm&logoWidth=18
[lgtm-alerts-url]: https://lgtm.com/projects/g/Stephen-RA-King/pynamer/alerts/
[lgtm-quality-image]: https://img.shields.io/lgtm/grade/python/g/Stephen-RA-King/pynamer.svg?logo=lgtm&logoWidth=18
[lgtm-quality-url]: https://lgtm.com/projects/g/Stephen-RA-King/pynamer/context:python
[license-image]: https://img.shields.io/pypi/l/pynamer
[license-url]: https://github.com/Stephen-RA-King/pynamer/blob/main/license
[mypy-image]: http://www.mypy-lang.org/static/mypy_badge.svg
[mypy-url]: http://mypy-lang.org/
[pre-commit-image]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[pre-commit-url]: https://github.com/pre-commit/pre-commit
[pre-commit.ci-image]: https://results.pre-commit.ci/badge/github/Stephen-RA-King/pynamer/main.svg
[pre-commit.ci-url]: https://results.pre-commit.ci/latest/github/Stephen-RA-King/pynamer/main
[pypi-url]: https://pypi.org/project/pynamer/
[pypi-image]: https://img.shields.io/pypi/v/pynamer.svg
[python-version-image]: https://img.shields.io/pypi/pyversions/pynamer
[readthedocs-image]: https://readthedocs.org/projects/pynamer/badge/?version=latest
[readthedocs-url]: https://pynamer.readthedocs.io/en/latest/?badge=latest
[status-image]: https://img.shields.io/pypi/status/pynamer.svg
[tests-image]: https://github.com/Stephen-RA-King/pynamer/actions/workflows/tests.yml/badge.svg
[tests-url]: https://github.com/Stephen-RA-King/pynamer/actions/workflows/tests.yml
[wiki]: https://github.com/Stephen-RA-King/pynamer/wiki
