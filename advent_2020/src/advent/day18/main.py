"""Day 17 of the advent of code challenge."""
from __future__ import annotations

import math
from pathlib import Path
from typing import Generator, List


def read_inputs(filename: str) -> Generator[str, None, None]:
    """Read in a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file, should be in the same folder as this module


    Yields
    ------
    line: str
        The next line of text
    """
    here: Path = Path(__file__).resolve().parent
    in_path: Path = here / filename
    with open(in_path, "r") as f:
        for line in f.readlines():
            yield line


def matching_brace_index(line: str) -> int:
    """Find the matching close parens of a string starting with open parens.

    Parameters
    ----------
    line: str
        line starting with (
    
    Returns
    -------
    int:
        The index of the character with the close parens
    """
    if not line.startswith("("):
        raise ValueError(f"{line} doesn't start with (")
    istart: List[int] = []
    for i, c in enumerate(line):
        if c == "(":
            istart.append(i)
        if c == ")":
            if len(istart) == 1:
                return i
            else:
                istart.pop()
    raise IndexError(f"Couldn't find closing parens for {line}")


def parse(line: str) -> str:
    """Parse a line using weird math.

    Parameters
    ----------
    line: str
        The input line
    
    Returns
    -------
    str
        The weird math output
    """
    if "(" in line:
        start_index: int = min(i for i, c in enumerate(line) if c == "(")
        end_index: int = matching_brace_index(line[start_index:]) + start_index
        cleaned_line = (
            line[:start_index]
            + str(parse(line[start_index + 1 : end_index]))
            + line[end_index + 1 :]
        )
        return parse(cleaned_line)
    else:
        equation: List[str] = list(reversed(line.split()))
        while len(equation) >= 3:
            num1: str = equation.pop()
            op: str = equation.pop()
            num2: str = equation.pop()
            equation.append(str(eval(" ".join((num1, op, num2)))))  # noqa:S307
        if len(equation) != 1:
            raise RuntimeError(f"Something dumb happened with {line}")
        return equation[0]


def parse2(line: str) -> str:
    """Parse a line using updated weird math.

    Could I factor out some common stuff from parse 1? Probably. Will I? No.

    Parameters
    ----------
    line: str
        The input line
    
    Returns
    -------
    str
        The weird math output
    """
    if "(" in line:
        start_index: int = min(i for i, c in enumerate(line) if c == "(")
        end_index: int = matching_brace_index(line[start_index:]) + start_index
        cleaned_line = (
            line[:start_index]
            + str(parse2(line[start_index + 1 : end_index]))
            + line[end_index + 1 :]
        )
        return parse2(cleaned_line)
    else:
        equation: List[str] = list(reversed(line.split()))
        while "+" in equation:
            next_plus: int = min(i for i, x in enumerate(equation) if x == "+")
            pre: List[str]
            post: List[str]
            try:
                pre = equation[: next_plus - 1]
            except IndexError:
                pre = []
            try:
                post = equation[next_plus + 2 :]
            except IndexError:
                post = []
            mid = [str(int(equation[next_plus - 1]) + int(equation[next_plus + 1]))]
            equation = pre + mid + post
        nums: List[int] = [int(x) for x in equation if x != "*"]
        return str(math.prod(nums))


def part1(filename: str = "input.txt") -> int:
    """Solve part 1 of the challenge.

    Parameters
    ----------
    filename: str
        The name of the file, should be in the same folder as this module

    Returns
    -------
    int
        The answer to part 1
    """
    return sum(int(parse(line)) for line in read_inputs(filename))


def part2(filename: str = "input.txt") -> int:
    """Solve part 2 of the challenge.

    Parameters
    ----------
    filename: str
        The name of the file, should be in the same folder as this module

    Returns
    -------
    int
        The answer to part 2
    """
    return sum(int(parse2(line)) for line in read_inputs(filename))
