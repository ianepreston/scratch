"""Advent of code 2021 day 13 puzzle."""
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple


class Point(NamedTuple):
    x: int
    y: int

    def __getitem__(self, item):
        """Access by string or integer for fields."""
        if isinstance(item, int):
            item = self._fields[item]
        return getattr(self, item)


class Fold(NamedTuple):
    axis: str
    point: int


def parse_instructions(infile: str) -> Tuple[List[Point], List[Fold]]:
    """Read in the puzzle instructions."""
    inpath = Path(__file__).resolve().parent / infile
    with open(inpath, "r") as f:
        puzzle = "".join(f.readlines())
    pointsstr, foldsstr = puzzle.split("\n\n")
    points = [
        Point(int(x.split(",")[0]), int(x.split(",")[1])) for x in pointsstr.split("\n")
    ]
    folds = [
        Fold(x.split("=")[0].replace("fold along ", ""), int(x.split("=")[1]))
        for x in foldsstr.split("\n")
    ]

    return points, folds


def make_grid(points: List[Point]) -> Dict[Point, int]:
    """Classic point mapping with a dictionary."""
    return {point: 1 for point in points}


def fold_point(point: Point, fold: Fold) -> Point:
    """Fold a point."""
    if point[fold.axis] < fold.point:
        return point
    elif point[fold.axis] > fold.point:
        if fold.axis == "x":
            newx = (2 * fold.point) - point.x
            return Point(newx, point.y)
        elif fold.axis == "y":
            newy = (2 * fold.point) - point.y
            return Point(point.x, newy)
    else:
        raise ValueError(f"Folds aren't supposed to happen right on a point.")


def fold_grid(grid: Dict[Point, int], fold: Fold) -> Dict[Point, int]:
    newgrid = dict()
    for point in grid.keys():
        newgrid[fold_point(point, fold)] = 1
    return newgrid


def part1(infile: str) -> int:
    points, folds = parse_instructions(infile)
    fold = folds[0]
    grid = make_grid(points)
    newgrid = fold_grid(grid, fold)
    return len(newgrid)


def print_grid(grid: Dict[Point, int]) -> None:
    xs = [point.x for point in grid.keys()]
    ys = [point.y for point in grid.keys()]
    minx = min(xs)
    maxx = max(xs)
    miny = min(ys)
    maxy = max(ys)
    listgrid = list()
    for y in range(miny, maxy + 1):
        row = "".join(
            "x" if Point(x, y) in grid.keys() else " " for x in range(minx, maxx + 1)
        )
        listgrid.append(row)
    strgrid = "\n".join(row for row in listgrid)
    print(strgrid)


def part2(infile: str) -> None:
    points, folds = parse_instructions(infile)
    grid = make_grid(points)
    for fold in folds:
        grid = fold_grid(grid, fold)
    print_grid(grid)


if __name__ == "__main__":
    eg1 = part1("example.txt")
    eg1a = 17
    if eg1 != eg1a:
        raise ValueError(f"Example 1 expected {eg1a} got {eg1}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")
    print("\n\n Part 2: \n\n")
    part2("example.txt")
    print("\n\n")
    part2("input.txt")
