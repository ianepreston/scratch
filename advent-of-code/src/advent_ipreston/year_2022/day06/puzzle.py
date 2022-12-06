"""Tuning Trouble."""
from advent_ipreston.helpers import inputs_generator


def get_input(infile: str) -> str:
    """Parse the input file to get the puzzle string."""
    return next(inputs_generator(infile))


def first_distinct_n(streambuffer: str, n: int = 4) -> int:
    """Find the index of the end of the first n nonrepeating characters."""
    for i in range(n, len(streambuffer)):
        if len(set(streambuffer[i - n : i])) == n:
            return i
    raise RuntimeError(f"Got to the end of the sequence without {n} unique.")


def part1(infile: str) -> int:
    """Solve part 1."""
    return first_distinct_n(get_input(infile), 4)


def part2(infile: str) -> int:
    """Solve part 1."""
    return first_distinct_n(get_input(infile), 14)
