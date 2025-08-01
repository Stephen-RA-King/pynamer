_**As a replacement for pip search, pynamer will quickly ascertain if a project name is 'available' in PyPI and optionally 'register' it.**_

[![PyPI][pypi-image]][pypi-url]
[![Downloads][downloads-image]][downloads-url]
[![Status][status-image]][pypi-url]
[![Python Version][python-version-image]][pypi-url]
[![tests][tests-image]][tests-url]
[![Codecov][codecov-image]][codecov-url]
[![CodeQl][codeql-image]][codeql-url]
[![Docker][docker-image]][docker-url]
[![pre-commit.ci status][pre-commit.ci-image]][pre-commit.ci-url]
[![readthedocs][readthedocs-image]][readthedocs-url]
[![CodeFactor][codefactor-image]][codefactor-url]
[![Codeclimate][codeclimate-image]][codeclimate-url]
[![Imports: isort][isort-image]][isort-url]
[![Code style: black][black-image]][black-url]
[![Checked with mypy][mypy-image]][mypy-url]
[![security: bandit][bandit-image]][bandit-url]
[![Commitizen friendly][commitizen-image]][commitizen-url]
[![Conventional Commits][conventional-commits-image]][conventional-commits-url]
[![DeepSource][deepsource-image]][deepsource-url]
[![license][license-image]][license-url]
[![pydough][pydough-image]][pydough-url]
<!-- [![OpenSSFScorecard][openssf-image]][openssf-url] -->



![](assets/pynamer1.png)

# Contents

-   [TL;DR](#-tldr)
-   [Demo](#-demo)
-   [Project Rationale](#-project-rationale)
-   [Quick Start](#-quick-start)
    -   [Prerequisites](#-prerequisites)
    -   [Installation](#-installation)
    -   [Basic Usage](#-basic-usage)
-   [Usage](#-usage)
    -   [Specifying multiple names](#specifying-multiple-names)
    -   [Using an input file](#using-an-input-file)
    -   [Saving the results to a file](#saving-the-results-to-a-file)
    -   [Display GitHub statistics](#display-github-statistics)
    -   [Register the name with PyPI](#register-the-package-name-with-pypi)
    -   [Verbose output](#verbose-output)
    -   [Regenerate the PyPI simple Repository Index](#regenerate-the-pypi-simple-repository-index)
-   [The oddities](#-the-oddities)
-   [Limitations](#-limitations)
-   [Using the Docker Image](#-using-the-docker-image)
-   [Documentation](#-documentation)
    -   [Read the Docs](https://pynamer.readthedocs.io/en/latest/)
    -   [API](https://pynamer.readthedocs.io/en/latest/autoapi/pynamer/pynamer/index.html)
    -   [Wiki](https://github.com/Stephen-RA-King/pynamer/wiki)
-   [Planned Future improvements](#-planned-future-improvements)
-   [Package Statistics](#-package-statistics)
-   [License](#-license)
-   [Meta Information](#ℹ-meta)


# 📺 Demo

![](assets/demo.gif)


# 💡 Project Rationale

Some of you may have reached the point where you want to publish a package in the PyPI python repository.
The first step of which is to choose a unique name. Here lies the problem.

A recent look at the PyPI repository revealed there were over 663,251 projects, so many names have already been taken.

pip leaps to the rescue with its search utility... or does it?

```python
pip search zaphod
```

```bash
ERROR: XMLRPC request failed [code: -32500]
RuntimeError: PyPI no longer supports 'pip search' (or XML-RPC search).
Please use https://pypi.org/search (via a browser) instead.
See https://warehouse.pypa.io/api-reference/xml-rpc.html#deprecated-methods for more information.
```

A quick search will show the internet replete with articles explaining the situation:

-   [The Register: Why Python's pip search isn't working](https://www.theregister.com/2021/05/25/pypi_search_error/)
-   [Python.org discussion: Pip search is still broken](https://discuss.python.org/t/pip-search-is-still-broken/18680)

OK so I go to the PyPI website and do a search for 'zaphod' as suggested by pip and 7 results are displayed none of which have the package name 'zaphod'

![](assets/pypi_zaphod.png)

Fantastic! I now think unbelievably that I have a unique name for a project that I can use.
So, I go ahead and code my new project, along with all the test files, documentation and meta data.
I diligently debug and commit and push to git and github so I have a history.

Finally the project is good enough to release and publish as an installable package on PyPI.

Here goes....

```bash
~ $ python -m twine upload --config-file .pypirc dist/*
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

Enter Pynamer. Pynamer does not rely on a single method of finding a PyPI package:

## 👓 TLDR

Pynamer uses the following methods to ascertain whether a package already exists on PyPI:

-   A simple request to the project url on PyPI.
-   Uses the PyPI "simple" repository - a text-based listing of all the packages available on PyPI.
-   Uses PyPI's own search 'API' and scrapes the results.

Pynamer provides a way to optionally 'register' a name on PyPI by building a minimalistic package and uploading

# 🚀 Quick Start

---

## 📋 Prerequisites

---

-   [x] Python >= 3.9.

The following are optional but required for 'registering' a project name on PyPI

-   [x] An account on PyPI (and generate a PyPI API token).
-   [x] A [**.pypirc**](https://packaging.python.org/en/latest/specifications/pypirc/) file containing your PyPI API token.

    or

-   [x] Configure [Twine environment variables](https://twine.readthedocs.io/en/latest/#environment-variables).

Your .pypirc file should contain the following and be on your PATH:

```file
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = your_API_token_here
```

## 💾 Installation

Pynamer can be installed into any python environment using pip:

```bash
~ $ pip install pynamer
```

However, optimal installation can be achieved using [**pipx**][pipx-url]:

```bash
~ $ pipx install pynamer
```

## 📝 Basic Usage

#### A package name that is not available

```bash
~ $ pynamer pynball
```

![](assets/usage_pynball.png)

#### A package name that is available

```bash
~ $ pynamer allitnil
```

![](assets/usage_available.png)

Holy smoke batman! You've managed to identify a unique name.

Yes, even though the odds were against you (given there are over 663,251 registered projects), you did it!

Even though the name has nothing in common with your project, or may not even be a real word... you did it!

Congratulations!

# 📝 Usage

---

Display the help menu with the `-h` argument

```bash
~ $ pynamer -h
```

```bash
usage: pynamer [-h] [-r] [-v] [-g] [-m] [-s] [-w] [-f FILENAME] [-o FILENAME] [--version] [projects ...]

Determine if project name is available on pypi with the option to 'register' it for future use if available

positional arguments:
  projects          Optional - one or more project names

optional arguments:
  -h, --help        show this help message and exit
  -r, --register    register the name on PyPi if the name is available
  -v, --verbose     display information about similar projects
  -g, --generate    generate a new PyPI index file
  -m, --meta        input new meta data when registering (Author and email address)
  -s, --stats       display GitHub stats if available
  -w, --webbrowser  open the project on PyPI in a webbrowser
  -f FILENAME       file containing a list of project names to analyze
  -o FILENAME       file to save the test results
  --version         display version number
```

## Specifying multiple names

You can specify as many names as you like from the command line e.g.

```bash
~ $ pynamer ganymede europa callisto
```

## Using an input file

You can use the `-f` argument to specify a file containing the a names of projects to analyze.
You specify a space separated sequence of as many names as you like on as many lines as you like. e.g.

'projects' file

```file
ganymede europa
IO callisto
```

Then specify the `-f` argument

```bash
~ $ pynamer -f projects
```

You can use the input file with names from the command line. The names will be aggregated. e.g.

```bash
~ $ pynamer ersa pandia leda metis -f projects
```

## Saving the results to a file

You can specify a file to write the result to by using the `-o` argument. e.g.

```bash
~ $ pynamer ersa pandia leda -o results
```

This will write a file e.g.

results

```file
Result from pynamer PyPI utility 2023-05-02
-------------------------------------------
test 1 - Basic url lookup on PyPI
test 2 - Search of PyPIs simple index
test 3 - Search using an request to PyPIs search 'API'.

Project name    Test1      Test2        Test 3          Conclusion
-------------------------------------------------------------------
ersa            Found       Found       Found           Not Available
pandia          Not Found   Not Found   Found           Not Available
leda            Not Found   Not Found   Not Found       Available
```

Again you can use a combination of names from the command line and input file.

## Display GitHub statistics

You can optionally display some of the most pertinent GitHub statistics if available by using the `-s` argument.
The statistics will be displayed in the the details section of test 1. e.g.

```bash
~ $ pynamer black -s
```

![](assets/usage_stats.png)

## Register the package name with PyPI

You can optionally 'register' the name on PyPI by using the `-r` argument.
If the project name is found to be available and you have a valid 'pypirc' file is found, a minimalistic project will be built and uploaded
to PyPI.

The first time you use the 'registration' procedure you will be prompted to enter your name and email address. These are required.
You can also optionally choose to change the version and description.

![](assets/usage_register_first.png)

This information will be retained and you will not be prompted to enter this information again. However, you can regenerate
this meta data by using the `-m` argument along with the `-r` argument. You can just enter on the options you dont want to change.

![](assets/usage_register_meta.png)

```bash
~ $ pynamer agrajag -r
```

![](assets/usage_register.png)

## Verbose output

With the `-v` argument you can display the first page of all other project matched by PyPIs search API - ordered by relevance.
The algorithm that PyPI uses to select these in unknown but seems to be a mixture of names and other
projects written by the same author.

```bash
~ $ pynamer pynamer -v
```

![](assets/usage_verbose.png)

## Regenerate the PyPI simple Repository Index

As one of its tests Pynamer makes use of a list of package names scraped from its simple index site.

The PyPI Simple Index is a plain text file that lists the names of all the packages available on PyPI.

It is a simplified version of the PyPI index that makes it easier for users to browse and download packages.

The PyPI Simple Index is used by a variety of tools and libraries to download and install packages from PyPI. For example, the pip package manager, which is used to install and manage Python packages, uses the PyPI Simple Index to find packages.
The Index is updated every few hours.

Using the `-g` argument can be used to regenerate the local file contents.

```bash
~ $ pynamer -g
```

![](assets/usage_generate.png)

See planned future improvements

# ⁉️ The Oddities

The reason I wrote this application in the first place...

```bash
~ $ pynamer zaphod
```

![](assets/usage_zaphod.png)

Even worse ...

```bash
~ $ pynamer zem
```

![](assets/usage_zem.png)

You may ask .. Why not just use the PyPI simple search index, that seems to be a pretty good indicator?
Well that is because it isn't...

```bash
~ $ pynamer gitmon
```

![](assets/usage_gitmon.png)


# ⚠️ Limitations

There will be occasions where all the tests pass, the name appears to be available but the upload to PyPI still fails.
This can be several reasons for this:

-   You are trying to use an internally "reserved" keyword for PyPI.
-   The name you are using is too similar to an existing project name and you get the following error message:

```bash
...
Error during upload. Retry with the --verbose option for more details.
HTTPError: 400 Bad Request from https://test.pypi.org/legacy/
The name 'yourpackage' is too similar to an existing project. See https://test.pypi.org/help/#project-name for more information-
```

Using a name similar to to an existing package name is a security issue.

Malicious players will try to create project names that are frequently mistyped for large popular projects, thereby facilitating installation of a malicious project.
e.g. replacing "L" / "l" with the number 1 or "o" / "O" with 0. The Software utilized by PyPI can be found on GitHub: [warehouse](https://github.com/pypi/warehouse).

# 🐳 Using the Docker Image

Pull the latest image from the Hub.
```bash
~ $ docker pull sraking/pynamer
```
Run the image.
```bash
~ $ docker run -it sraking/pynamer /bin/bash
```
Use the command line as normal in the container.

```bash
root@4d315992ca28:/app# pynamer
usage: pynamer [-h] [-r] [-v] [-g] [-m] [-s] [-w] [-f FILENAME] [-o FILENAME] [--version] [projects ...]

Determine if project name is available on pypi with the option to 'register' it for future use if available
...
```



# 📚 Documentation

---

[**Read the Docs**](https://pynamer.readthedocs.io/en/latest/)

-   [**Credits**](https://pynamer.readthedocs.io/en/latest/example.html)
-   [**Changelog**](https://pynamer.readthedocs.io/en/latest/changelog.html)
-   [**API Reference**](https://pynamer.readthedocs.io/en/latest/autoapi/index.html)

[**Wiki**](https://github.com/Stephen-RA-King/pynamer/wiki)

# 📆 Planned Future improvements

---

-   Improve performance of the regeneration of the PyPI simple Repository Index, so this can be run in the background automatically.


# 📊 Package Statistics

---

- [**libraries.io**](https://libraries.io/pypi/pynamer)
- [**PyPI Stats**](https://pypistats.org/packages/pynamer)
- [**Pepy**](https://www.pepy.tech/projects/pynamer)


# 📜 License

Distributed under the MIT license. See [![][license-image]][license-url] for more information.



# <ℹ️> Meta

---

[![Linkedin](assets/linkedin.png)](https://www.linkedin.com/in/sr-king)
[![](assets/github.png)](https://github.com/Stephen-RA-King)
[![PyPI repository](assets/pypi.png)](https://pypi.org/project/pynamer)
[![Docker](assets/docker.png)](https://hub.docker.com/r/sraking/pynamer)
[![](assets/www.png)](https://stephen-ra-king.github.io/justpython/)
[![](assets/email2.png)](mailto:sking.github@gmail.com)

Author: Stephen King  ([sking.github@gmail.com](mailto:sking.github@gmail.com))

Created with Cookiecutter template: [![pydough][pydough-image]][pydough-url] version 1.2.2

Digital object identifier: [![DOI](https://zenodo.org/badge/631029310.svg)](https://zenodo.org/badge/latestdoi/631029310)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8104298.svg)](https://doi.org/10.5281/zenodo.8104298)



<!-- Markdown link & img dfn's -->

[bandit-image]: https://img.shields.io/badge/security-bandit-yellow.svg
[bandit-url]: https://github.com/PyCQA/bandit
[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[codeclimate-image]: https://api.codeclimate.com/v1/badges/b95fb617fbcd469ccfc3/maintainability
[codeclimate-url]: https://codeclimate.com/github/Stephen-RA-King/pynamer/maintainability
[codeclimate-url]: https://codeclimate.com/github/Stephen-RA-King/pynamer/maintainability
[codecov-image]: https://codecov.io/gh/Stephen-RA-King/pynamer/branch/main/graph/badge.svg
[codecov-url]: https://app.codecov.io/gh/Stephen-RA-King/pynamer
[codefactor-image]: https://www.codefactor.io/repository/github/Stephen-RA-King/pynamer/badge
[codefactor-url]: https://www.codefactor.io/repository/github/Stephen-RA-King/pynamer
[codeql-image]: https://github.com/Stephen-RA-King/pynamer/actions/workflows/codeql.yml/badge.svg
[codeql-url]: https://github.com/Stephen-RA-King/pynamer/actions/workflows/codeql.yml
[commitizen-image]: https://img.shields.io/badge/commitizen-friendly-brightgreen.svg
[commitizen-url]: http://commitizen.github.io/cz-cli/
[conventional-commits-image]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square
[conventional-commits-url]: https://conventionalcommits.org
[deepsource-image]: https://app.deepsource.com/gh/Stephen-RA-King/pynamer.svg/?label=active+issues&show_trend=true&token=SGo-Vr17NUYVQaEWkU9rBb6Y
[deepsource-url]: https://app.deepsource.com/gh/Stephen-RA-King/pynamer/?ref=repository-badge
[docker-image]: https://github.com/Stephen-RA-King/pynamer/actions/workflows/docker-image.yml/badge.svg
[docker-url]: https://github.com/Stephen-RA-King/pynamer/actions/workflows/docker-image.yml
[downloads-image]: https://static.pepy.tech/personalized-badge/pynamer?period=total&left_color=black&right_color=blue&left_text=Downloads
[downloads-url]: https://pepy.tech/project/pynamer
[format-image]: https://img.shields.io/pypi/format/pynamer
[isort-image]: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336?
[isort-url]: https://github.com/pycqa/isort/
[lgtm-alerts-image]: https://img.shields.io/lgtm/alerts/g/Stephen-RA-King/pynamer.svg?logo=lgtm&logoWidth=18
[lgtm-alerts-url]: https://lgtm.com/projects/g/Stephen-RA-King/pynamer/alerts/
[lgtm-quality-image]: https://img.shields.io/lgtm/grade/python/g/Stephen-RA-King/pynamer.svg?logo=lgtm&logoWidth=18
[lgtm-quality-url]: https://lgtm.com/projects/g/Stephen-RA-King/pynamer/context:python
[license-image]: https://img.shields.io/pypi/l/pynamer
[license-url]: https://github.com/Stephen-RA-King/pynamer/blob/main/LICENSE
[mypy-image]: http://www.mypy-lang.org/static/mypy_badge.svg
[mypy-url]: http://mypy-lang.org/
[openssf-image]: https://api.securityscorecards.dev/projects/github.com/Stephen-RA-King/pynamer/badge
[openssf-url]: https://api.securityscorecards.dev/projects/github.com/Stephen-RA-King/pynamer
[pipx-url]: https://pypa.github.io/pipx/
[pre-commit-image]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[pre-commit-url]: https://github.com/pre-commit/pre-commit
[pre-commit.ci-image]: https://results.pre-commit.ci/badge/github/Stephen-RA-King/pynamer/main.svg
[pre-commit.ci-url]: https://results.pre-commit.ci/latest/github/Stephen-RA-King/pynamer/main
[pydough-image]: https://img.shields.io/badge/pydough-2023-orange?logo=cookiecutter
[pydough-url]: https://github.com/Stephen-RA-King/pydough
[pypi-image]: https://img.shields.io/pypi/v/pynamer?logo=pypi&logoColor=lightblue
[pypi-url]: https://pypi.org/project/pynamer/
[python-version-image]: https://img.shields.io/pypi/pyversions/pynamer?logo=pypi&logoColor=lightblue
[readthedocs-image]: https://readthedocs.org/projects/pynamer/badge/?version=latest
[readthedocs-url]: https://pynamer.readthedocs.io/en/latest/?badge=latest
[status-image]: https://img.shields.io/pypi/status/pynamer?logo=pypi&logoColor=lightblue
[tests-image]: https://github.com/Stephen-RA-King/pynamer/actions/workflows/tests.yml/badge.svg
[tests-url]: https://github.com/Stephen-RA-King/pynamer/actions/workflows/tests.yml
[wiki]: https://github.com/Stephen-RA-King/pynamer/wiki
