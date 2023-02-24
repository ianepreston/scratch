"""Camp Cleanup."""
from typing import NamedTuple
from typing import Tuple

from advent_ipreston.helpers import inputs_generator


class Assignment(NamedTuple):
    """Lower and upper range of an elf's assignment."""

    lower: int
    upper: int


def parse_assignment_pair(pairline: str) -> Tuple[Assignment, Assignment]:
    """Turn a puzzle input line into a pair of assignents."""
    l, r = pairline.split(",")
    l_assingment = Assignment(*(int(x) for x in l.split("-")))
    r_assingment = Assignment(*(int(x) for x in r.split("-")))
    return (l_assingment, r_assingment)


def check_complete_overlap(assignments: Tuple[Assignment, Assignment]) -> bool:
    """Check if one assignment is subsumed in another."""
    l, r = assignments
    # Swap if necessary so l always starts equal to or below r
    if l.lower > r.lower:
        l, r = r, l
    if l.lower < r.lower:
        return r.upper <= l.upper
    # If they start at the same point they're identical or one fits in the other.
    else:
        return True


def check_overlap(assignments: Tuple[Assignment, Assignment]) -> bool:
    """Check if assignments have any overlap."""
    l, r = assignments
    # Swap if necessary so l always starts equal to or below r
    if l.lower > r.lower:
        l, r = r, l
    return any(
        (
            l.lower == r.lower,
            l.upper == r.upper,
            r.lower <= l.upper,
        )
    )


def part1(infile: str) -> int:
    """Solve part 1."""
    return sum(
        check_complete_overlap(parse_assignment_pair(pairline))
        for pairline in inputs_generator(infile)
    )


def part2(infile: str) -> int:
    """Solve part 1."""
    return sum(
        check_overlap(parse_assignment_pair(pairline))
        for pairline in inputs_generator(infile)
    )
