"""Day 09 of the advent of code challenge."""
from __future__ import annotations

from pathlib import Path
from typing import List, Set


def read_inputs(filename: str = "input.txt") -> List[int]:
    """Read in and parse a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    list[int]
        The numbers in the series
    """
    in_path: Path = Path(__file__).resolve().parent / filename
    with open(in_path, "r") as f:
        return [int(line.strip()) for line in f.readlines()]


def part1(filename: str = "input.txt", preamble_length: int = 25) -> int:
    """Solve part 1 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load
    preamble_length: int
        How many earlier characters to consider

    Returns
    -------
    int:
        The number that doesn't match the pattern
    """
    num_list: List[int] = read_inputs(filename)
    for index in range(preamble_length, len(num_list)):
        target: int = num_list[index]
        has: Set = {num_list[i] for i in range(index - preamble_length, index)}
        wants: Set = {
            target - num_list[i] for i in range(index - preamble_length, index)
        }
        if len(has.intersection(wants)) < 2:
            return target
    raise RuntimeError("Went through the whole list without solving part 1")


def part2(filename: str = "input.txt", preamble_length: int = 25) -> int:
    """Solve part 2 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load
    preamble_length: int
        How many earlier characters to consider to find the target number

    Returns
    -------
    int:
        The answer to part 2
    """
    num_list: List[int] = read_inputs(filename)
    target: int = part1(filename, preamble_length)
    low_index: int = 0
    high_index: int = 1
    while high_index < len(num_list):
        test_range: List[int] = num_list[low_index:high_index]
        range_sum: int = sum(test_range)
        if range_sum < target:
            high_index += 1
        elif range_sum > target:
            low_index += 1
        else:
            return min(test_range) + max(test_range)
    raise RuntimeError("Went through the whole list without solving part 2")
