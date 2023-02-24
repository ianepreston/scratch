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


def react(poly: str, reactions: Dict[str, str], steps: int) -> Dict[str, int]:
    """Run through the reactions."""
    lcounter = Counter(poly)
    pcounter = Counter("".join((a, b)) for a, b in zip(poly, poly[1:]))
    for _ in range(steps):
        for pair, count in Counter(pcounter).items():
            reaction = reactions[pair]
            if reaction:
                lpair = "".join((pair[0], reaction))
                rpair = "".join((reaction, pair[1]))
                pcounter[lpair] += count
                pcounter[rpair] += count
                pcounter[pair] -= count
                lcounter[reaction] += count
    return lcounter


def polydiff(lcounter: Dict[str, int]) -> int:
    """Difference between the count of the most common and least common element."""
    cmin, *_, cmax = sorted(lcounter.values())
    return cmax - cmin


def partn(infile: str, steps: int) -> int:
    polystr, react_dict = parse_input(infile)
    lcounter = react(polystr, react_dict, steps)
    return polydiff(lcounter)


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
