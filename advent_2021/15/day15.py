"""Advent of code 2021 day 15 challenge."""
from heapq import heapify, heappop, heappush
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


def dest_coord(grid: Grid) -> Coord:
    """Find the lower right corner of your grid."""
    x = max(coord[0] for coord in grid.keys())
    y = max(coord[1] for coord in grid.keys())
    return (x, y)


def scale_risks(risks: Grid, scale: int = 5) -> Grid:
    """Grow the risk dictionary for part 2."""
    scaled_risks = dict()
    mx, my = dest_coord(risks)
    for yscale in range(scale):
        for xscale in range(scale):
            for ocoord, orisk in risks.items():
                newx = ((mx + 1) * xscale) + ocoord[0]
                newy = ((my + 1) * yscale) + ocoord[1]
                newrisk = orisk + xscale + yscale
                # There absolutely has to be a better way to do this
                while newrisk > 9:
                    newrisk = newrisk - 9
                scaled_risks[(newx, newy)] = newrisk
    return scaled_risks


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


def travel_grid(risks: Grid) -> Grid:
    """Get travel cost from source to every other point."""
    costs = init_travel_costs(riskdict=risks)
    visited = set()
    candidates = [
        (v, k) for k, v in costs.items() if k not in visited and v != float("inf")
    ]
    heapify(candidates)
    while len(visited) < len(risks):
        # Find lowest cost unvisited point as the next point to visit
        visit_point = heappop(candidates)[1]
        for neighbour in neighbours(visit_point, risks):
            oldcost = costs[neighbour]
            costs[neighbour] = min(
                (costs[neighbour], (costs[visit_point] + risks[neighbour]))
            )
            if costs[neighbour] < oldcost:
                heappush(candidates, (costs[neighbour], neighbour))
        visited.add(visit_point)
    return costs


def part1(infile: str) -> Number:
    risks = read_risks(infile)
    costs = travel_grid(risks)
    dest = dest_coord(costs)
    return costs[dest]


def part2(infile: str) -> Number:
    risks = scale_risks(read_risks(infile), 5)
    costs = travel_grid(risks)
    dest = dest_coord(costs)
    return costs[dest]


if __name__ == "__main__":
    eg1 = part1("example.txt")
    eg1a = 40
    if eg1 != eg1a:
        raise ValueError(f"Expected {eg1a}, got {eg1}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")
    eg2 = part2("example.txt")
    eg2a = 315
    if eg2 != eg2a:
        raise ValueError(f"Expected {eg2a}, got {eg2}")
    a2 = part2("input.txt")
    print(f"Part 2: {a2}")
