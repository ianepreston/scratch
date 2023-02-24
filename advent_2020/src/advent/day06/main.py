"""Day 06 of the advent of code challenge."""
from __future__ import annotations

from pathlib import Path
from typing import Generator, Set


def read_inputs(filename: str = "input.txt") -> Generator[Set, None, None]:
    """Read in and parse a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Yields
    ------
    Set
        All questions answered "yes" at least once on the questionnaire per group
    """
    here: Path = Path(__file__).resolve().parent
    in_path: Path = here / filename
    with open(in_path, "r") as f:
        for line in f.read().split("\n\n"):
            yield set(char for char in line.replace("\n", ""))


def part1(filename: str = "input.txt") -> int:
    """Count the sum of unique answers for all groups.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    int:
        The sum of all unique answers
    """
    return sum(len(result) for result in read_inputs(filename))


def read_inputs2(filename: str = "input.txt") -> Generator[Set, None, None]:
    """Read in and parse a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Yields
    ------
    Set
        All questions answered "yes" at least once on the questionnaire per group
    """
    here: Path = Path(__file__).resolve().parent
    in_path: Path = here / filename
    with open(in_path, "r") as f:
        for group in f.read().split("\n\n"):
            yield set.intersection(
                *(set(char for char in line) for line in group.split("\n"))
            )


def part2(filename: str = "input.txt") -> int:
    """Count the sum of answers everyone in the group answered yes to.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    int:
        The sum of all answers everyone in the group answered yes to
    """
    return sum(len(result) for result in read_inputs2(filename))
