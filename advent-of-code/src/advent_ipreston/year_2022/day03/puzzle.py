"""Rucksack Reorganization."""
import itertools
import string
from typing import Generator

from advent_ipreston.helpers import inputs_generator


def split_compartments(rucksack: str) -> tuple[set[str], set[str]]:
    """Split the rucksack into two compartments."""
    midpoint = len(rucksack) // 2
    front = set(rucksack[:midpoint])
    back = set(rucksack[-midpoint:])
    return front, back


def find_common(front: set[str], back: set[str]) -> str:
    """Find the element common in both rucksacks."""
    common = front.intersection(back)
    if len(common) != 1:
        raise RuntimeError(f"Wrong number of common elements: {common}")
    return common.pop()


def find_priority(letter: str) -> int:
    """Map the letter value to a priority."""
    priorities = {c: n + 1 for n, c in enumerate(string.ascii_letters)}
    return priorities[letter]


def prioritize_rucksack(rucksack: str) -> int:
    """Split, find common letter, find priority for a rucksack."""
    front, back = split_compartments(rucksack)
    common = find_common(front, back)
    return find_priority(common)


def part1(infile: str) -> int:
    """Solve part 1."""
    return sum(prioritize_rucksack(rucksack) for rucksack in inputs_generator(infile))


def group_rucksacks(
    infile: str,
) -> Generator[tuple[set[str], set[str], set[str]], None, None]:
    """Get the rucksacks in groups of three."""
    rucksack_generator = inputs_generator(infile)
    while rucksack_generator:
        groups = tuple(set(x) for x in itertools.islice(rucksack_generator, 3))
        if len(groups) == 3:
            yield groups
        else:
            break


def find_common_rucksacks(rucksacks: tuple[set[str], set[str], set[str]]) -> str:
    """Find the element common among three rucksacks."""
    a, b, c = rucksacks
    common = a.intersection(b).intersection(c)
    if len(common) != 1:
        raise RuntimeError(f"Wrong number of common elements: {common}")
    return common.pop()


def prioritize_rucksacks(rucksacks: tuple[set[str], set[str], set[str]]) -> int:
    """Take three rucksacks and find their priority."""
    common = find_common_rucksacks(rucksacks)
    return find_priority(common)


def part2(infile: str) -> int:
    """Solve part 2."""
    return sum(prioritize_rucksacks(rucksacks) for rucksacks in group_rucksacks(infile))
