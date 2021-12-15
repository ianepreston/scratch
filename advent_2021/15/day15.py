"""Advent of code 2021 day 15 challenge."""
from pathlib import Path
from typing import Dict, List, Tuple, Union

Number = Union[int, float]
Coord = Tuple[int, int]
Grid = Dict[Coord, Number]


def read_risks(infile: str) -> Grid:
    """Read in the risk grid."""
    inpath = Path(__file__).resolve().parent / infile
    with open(inpath, "r") as f:
        return {
            (x, y): int(char)
            for y, line in enumerate(f.readlines())
            for x, char in enumerate(line.strip())
        }


def init_travel_costs(riskdict: Grid) -> Grid:
    """Make estimated travel cost infinite to start."""
    tc = {coord: float("inf") for coord in riskdict.keys()}
    # Start point has 0 travel cost
    tc[(0, 0)] = 0
    return tc


def neighbours(coord: Coord, grid: Grid) -> List[Coord]:
    vecs = (-1, 0, 1)
    return [
        (xvec + coord[0], yvec + coord[1])
        for xvec in vecs
        for yvec in vecs
        # Don't want 0, 0 or any diagonals
        if (bool(xvec) != bool(yvec))
        and ((xvec + coord[0], yvec + coord[1]) in grid.keys())
    ]


def dest_coord(grid: Grid) -> Coord:
    x = max(coord[0] for coord in grid.keys())
    y = max(coord[1] for coord in grid.keys())
    return (x, y)


def travel_grid(infile: str) -> Grid:
    """Get travel cost from source to every other point."""
    risks = read_risks(infile)
    costs = init_travel_costs(riskdict=risks)
    visited = set()
    while len(visited) < len(risks):
        # Find lowest cost unvisited point as the next point to visit
        visit_point = [
            k
            for k, _ in sorted(costs.items(), key=lambda item: item[1])
            if k not in visited
        ][0]
        for neighbour in neighbours(visit_point, risks):
            costs[neighbour] = min(
                (costs[neighbour], (costs[visit_point] + risks[neighbour]))
            )
        visited.add(visit_point)
    return costs


def part1(infile: str) -> Number:
    costs = travel_grid(infile)
    dest = dest_coord(costs)
    return costs[dest]


if __name__ == "__main__":
    eg1 = part1("example.txt")
    eg1a = 40
    if eg1 != eg1a:
        raise ValueError(f"Expected {eg1a}, got {eg1}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")
