# Core Library modules
import argparse


def _parse_args(args: list) -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    """Function to return the ArgumentParser object created from all the args.

    Args:
        args:   A list of arguments from the commandline
                e.g. ['pynball', '-v', '-g']
    """
    parser = argparse.ArgumentParser(
        prog="pynamer",
        description="Determine if project name is available on pypi with the "
        "option to 'register' it for future use if available",
    )
    parser.add_argument(
        "projects",
        nargs="*",
        default="None",
        help="Optional - one or more project names",
    )
    parser.add_argument(
        "-r",
        "--register",
        action="store_true",
        help="register the name on PyPi if the name is available",
    )
    parser.add_argument(
        "-d",
        "--dryrun",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-n",
        "--nocleanup",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="display information about similar projects",
    )
    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="generate a new PyPI index file",
    )
    parser.add_argument(
        "-m",
        "--meta",
        action="store_true",
        help="input new meta data when registering (Author and email address)",
    )
    parser.add_argument(
        "-s",
        "--stats",
        action="store_true",
        help="display GitHub stats if available",
    )
    parser.add_argument(
        "-w",
        "--webbrowser",
        action="store_true",
        help="open the project on PyPI in a webbrowser",
    )
    parser.add_argument(
        "-f",
        metavar="FILENAME",
        default="None",
        type=str,
        help="file containing a list of project names to analyze",
    )
    parser.add_argument(
        "-o",
        metavar="FILENAME",
        default="None",
        type=str,
        help="file to save the test results",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="display version number",
    )
    return parser.parse_args(args), parser
