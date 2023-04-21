#!/usr/bin/env python3
"""Example CLI module using click package."""


# Third party modules
import click


@click.group()
def info() -> None:
    """Create a container to which other commands can be attached."""


@info.command(help="Display Author Name")
@click.option("-verbose", "--verbose", is_flag=True, help="set the verbosity")
def author(verbose: str) -> None:
    """Returns details about the Author."""
    click.echo("Author name: Stephen R A King")
    if verbose:
        click.echo("Author eMail: sking.github@gmail.com")


if __name__ == "__main__":
    raise SystemExit(info())
