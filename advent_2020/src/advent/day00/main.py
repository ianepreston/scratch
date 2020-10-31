"""Day 1 of the 2019 advent, used for testing my 2020 repo in advance of the challenge."""
from pathlib import Path
from typing import Callable, Union

INFILE: Path = Path(__file__).parent / "input.txt"


def solver(fuel_func: Callable[[int], int], infile: Union[str, Path] = INFILE) -> int:
    """Use some fuel calculation function and apply it to an input list of part weights.

    Parameters
    ----------
    fuel_func: callable
        The function that will calculate fuel from mass
    infile: str or Path
        The file with a list of masses to read in

    Returns
    -------
    int
        Total fuel required based on fuel func and input masses
    """
    total_fuel: int = 0
    with open(infile, "r") as f:
        for line in f.readlines():
            total_fuel += fuel_func(int(line))
    return total_fuel


def calc_fuel(num: int) -> int:
    """Perform fuel calculation used in part1 of the challenge.

    Parameters
    ----------
    num: int
        Mass to calculate fuel requirement

    Returns
    -------
    int
        The amount of fuel required
    """
    return (num // 3) - 2


def recursive_fuel(num: int) -> int:
    """Perform fuel calculation used in part2 of the challenge.

    Parameters
    ----------
    num: int
        Mass to calculate fuel requirement

    Returns
    -------
    int
        The amount of fuel required
    """
    base = calc_fuel(num)
    if base <= 0:
        return 0
    else:
        return base + recursive_fuel(base)


def part1() -> int:
    """Run part 1 of the day 0 challenge.

    Returns
    -------
    int
        The solution to day 0 part 1
    """
    return solver(calc_fuel)


def part2() -> int:
    """Run part 2 of the day 0 challenge.

    Returns
    -------
    int
        The solution to day 0 part 2
    """
    return solver(recursive_fuel)
