"""Advent of code 2021 day 12."""
from collections import defaultdict
from pathlib import Path
from typing import Callable, Dict, List, Set


def map_connections(infile: str) -> Dict[str, Set[str]]:
    """Map where you can get from any point in the path."""
    pathdict = defaultdict(set)
    inpath = Path(__file__).resolve().parent / infile
    with open(inpath, "r") as f:
        for line in f.readlines():
            a, b = line.strip().split("-")
            pathdict[a].add(b)
            pathdict[b].add(a)
    # Can't go anywhere once you reach the end
    pathdict["end"] = set()
    return pathdict


def can_visitp1(cave: str, visited: List[str]) -> bool:
    """Check if we can visit a cave based on if it's small/visited."""
    # either we haven't visited a small cave, or it's big so we can revisit
    return (cave not in visited) or (cave.upper() == cave)


def can_visitp2(cave: str, visited: List[str]) -> bool:
    """Check if we can visit a cave based on part 2 criteria."""
    # Still no rules for large caves
    if cave.upper() == cave:
        return True
    # Can't go back to the start
    elif cave == "start":
        return False
    elif cave not in visited:
        return True
    else:
        lower_visited = [cave for cave in visited if cave == cave.lower()]
        # if we've visited each small cave once we can add another small one
        return len(lower_visited) == len(set(lower_visited))


def find_paths(infile: str, visitfunc: Callable) -> List[str]:
    """Find all the paths in a cave network."""
    pathdict = map_connections(infile)
    completed_paths = list()
    candidate_paths = [["start"]]
    while candidate_paths:
        candidate_path = candidate_paths.pop()
        new_routes = [
            cave
            for cave in pathdict[candidate_path[-1]]
            if visitfunc(cave, candidate_path)
        ]
        if new_routes:
            for new_route in new_routes:
                new_candidate = candidate_path + [new_route]
                candidate_paths.append(new_candidate)
        else:
            completed_paths.append(candidate_path)
    return completed_paths


def part1(infile: str) -> int:
    """Solve part 1."""
    good_paths = [path for path in find_paths(infile, can_visitp1) if "end" in path]
    return len(good_paths)


def part2(infile: str) -> int:
    """Solve part 2."""
    good_paths = [path for path in find_paths(infile, can_visitp2) if "end" in path]
    return len(good_paths)


if __name__ == "__main__":
    examples = [
        ("eg1.txt", 10),
        ("eg2.txt", 19),
        ("eg3.txt", 226),
    ]
    for example in examples:
        egf, ega = example
        eg = part1(egf)
        if eg != ega:
            raise ValueError(f"Example {egf} expected {ega}, got {eg}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")
    examples = [
        ("eg1.txt", 36),
        ("eg2.txt", 103),
        ("eg3.txt", 3509),
    ]
    for example in examples:
        egf, ega = example
        eg = part2(egf)
        if eg != ega:
            raise ValueError(f"Example {egf} expected {ega}, got {eg}")
    a2 = part2("input.txt")
    print(f"Part 2: {a2}")
