"""Advent of code 2021 day 14 puzzle."""
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Tuple


def parse_input(infile: str) -> Tuple[str, Dict[str, str]]:
    """Read in the input text file."""
    inpath = Path(__file__).resolve().parent / infile
    with open(inpath, "r") as f:
        instr = f.read()
    polystr, reactions = instr.split("\n\n")
    react_dict = defaultdict(str)
    for reaction in reactions.split("\n"):
        pair, mid = reaction.split(" -> ")
        react_dict[pair] = mid
    return polystr, react_dict


def react(poly: str, reactions: Dict[str, str]) -> str:
    """Create a chain reaction."""
    reaction_chain = "".join(
        "".join((a, reactions["".join((a, b))])) for a, b in zip(poly, poly[1:])
    )
    return "".join((reaction_chain, poly[-1]))


def polydiff(poly: str) -> int:
    """Difference between the count of the most common and least common element."""
    polylist = [c for c in poly]
    counts = Counter(polylist)
    maxcount = counts[max(polylist, key=counts.get)]
    mincount = counts[min(polylist, key=counts.get)]
    return maxcount - mincount


def partn(infile: str, steps: int) -> int:
    polystr, react_dict = parse_input(infile)
    for _ in range(steps):
        polystr = react(polystr, react_dict)
    return polydiff(polystr)


def part1(infile: str) -> int:
    return partn(infile, 10)


def part2(infile: str) -> int:
    return partn(infile, 40)


if __name__ == "__main__":
    eg1 = part1("example.txt")
    eg1a = 1588
    if eg1 != eg1a:
        raise ValueError(f"Expected {eg1a}, got {eg1}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")
    eg2 = part2("example.txt")
    eg2a = 2188189693529
    if eg2 != eg2a:
        raise ValueError(f"Expected {eg2a}, got {eg2}")
    a2 = part2("input.txt")
    print(f"Part 2: {a2}")
