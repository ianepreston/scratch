"""Advent of code 2021 Day 17 puzzle."""
from pathlib import Path
from typing import NamedTuple


class Bounds(NamedTuple):
    xmin: int
    xmax: int
    ymin: int
    ymax: int


def get_bounds(infile: str) -> Bounds:
    inpath = Path(__file__).resolve().parent / infile
    with open(inpath, "r") as f:
        line = f.readline().strip().replace("target area: ", "")
    xrange, yrange = line.split(", ")
    xmin, xmax = (int(c) for c in xrange.replace("x=", "").split(".."))
    ymin, ymax = (int(c) for c in yrange.replace("y=", "").split(".."))
    return Bounds(xmin, xmax, ymin, ymax)


def get_hmax(bounds: Bounds) -> int:
    ymin = bounds.ymin
    return abs(ymin) * abs(ymin + 1) // 2


def part1(infile: str) -> int:
    bounds = get_bounds(infile)
    return get_hmax(bounds)


def get_vecbounds(tbounds: Bounds) -> Bounds:
    ymin = tbounds.ymin
    ymax = abs(tbounds.ymin)
    xmax = tbounds.xmax
    xmin = 0
    # brute force hacky but whatever
    xdisplacement = (xmin * (xmin + 1)) // 2
    while xdisplacement < tbounds.xmin:
        xmin += 1
        xdisplacement = (xmin * (xmin + 1)) // 2
    return Bounds(xmin, xmax, ymin, ymax)


def check_target(xvec: int, yvec: int, tbounds: Bounds) -> bool:
    """Do we hit our target?"""
    x = 0
    y = 0
    while (x <= tbounds.xmax) and (y >= tbounds.ymin):
        x += xvec
        y += yvec
        xvec = max((0, xvec - 1))
        yvec -= 1
        if (tbounds.xmin <= x <= tbounds.xmax) and (tbounds.ymin <= y <= tbounds.ymax):
            return True
    return False


def part2(infile: str) -> int:
    tbounds = get_bounds(infile)
    vbounds = get_vecbounds(tbounds)
    xrange = range(vbounds.xmin, vbounds.xmax + 1)
    yrange = range(vbounds.ymin, vbounds.ymax + 1)
    return sum(check_target(x, y, tbounds) for x in xrange for y in yrange)


if __name__ == "__main__":
    eg1 = part1("example.txt")
    eg1a = 45
    if eg1 != eg1a:
        raise RuntimeError(f"Expected {eg1a}, got {eg1}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")
    eg2 = part2("example.txt")
    eg2a = 112
    if eg2 != eg2a:
        raise RuntimeError(f"Expected {eg2a}, got {eg2}")
    a2 = part2("input.txt")
    print(f"Part 2: {a2}")
