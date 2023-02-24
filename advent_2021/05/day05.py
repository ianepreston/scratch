"""Advent of code 2021 Day 05 challenge."""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple


class Point(NamedTuple):
    """Define a point in 2D space."""

    x: int
    y: int


class Slope(NamedTuple):
    """Define rise and run of a line segment in 2D space."""

    rise: int
    run: int


class LineSegment(NamedTuple):
    """Sequence of points in a line segment and an indicator if it's diagonal."""

    points: Tuple[Point]
    is_diagional: bool


def parse_point(coordstr: str) -> Point:
    """Make a point str like '1,2' into a Point namedtuple."""
    x, y = (int(coord) for coord in coordstr.split(","))
    return Point(x, y)


def parse_line(line: str) -> Tuple[Point, Point]:
    """Read a line from puzzle input and get its two points."""
    a_str, b_str = line.split(" -> ")
    a = parse_point(a_str)
    b = parse_point(b_str)
    return a, b


def check_is_diagonal(a: Point, b: Point) -> bool:
    """See if two points form a diagonal as opposed to horizontal or vertical line."""
    return (a.x != b.x) and (a.y != b.y)


def calc_slope(a: Point, b: Point) -> Slope:
    """Get rise and run of a slope."""
    # Fraction always puts the sign on numerator so we have to figure out
    # where to put it in advance
    if a.x > b.x:
        rundir = -1
    else:
        rundir = 1
    if a.y > b.y:
        risedir = -1
    else:
        risedir = 1
    if a.x == b.x:
        slope = Slope(risedir, 0)
    elif a.y == b.y:
        slope = Slope(0, rundir)
    else:
        total_rise = a.y - b.y
        total_run = a.x - b.x
        rise_run = Fraction(total_rise, total_run).limit_denominator()
        absrise = abs(rise_run.numerator)
        absrun = abs(rise_run.denominator)
        rise = absrise * risedir
        run = absrun * rundir
        slope = Slope(rise, run)
    return slope


def calc_contact_points(a: Point, b: Point) -> Tuple[Point]:
    """Get all grid coordinates a line segment touches."""
    rise, run = calc_slope(a, b)
    current_point = a
    contact_points = [a]
    while current_point != b:
        newx = current_point.x + run
        newy = current_point.y + rise
        current_point = Point(newx, newy)
        contact_points.append(current_point)
    return tuple(contact_points)


def create_line_segment(line: str) -> LineSegment:
    """Turn a puzzle input line into a LineSegment object."""
    a, b = parse_line(line)
    is_diagonal = check_is_diagonal(a, b)
    points = calc_contact_points(a, b)
    return LineSegment(points, is_diagonal)


def read_input(infile: str) -> List[LineSegment]:
    """Read in a puzzle input file and get back a list of line segments."""
    in_path = Path(__file__).resolve().parent / infile
    with open(in_path, "r") as f:
        return [create_line_segment(line) for line in f.readlines()]


def count_overlaps(
    segments: List[LineSegment], no_diagonals: bool = True
) -> Dict[Point, int]:
    """Get a dictionary counting how many line segments lie on each Point."""
    point_counter = defaultdict(int)
    if no_diagonals:
        check_segments = [segment for segment in segments if not segment.is_diagional]
    else:
        check_segments = segments
    for segment in check_segments:
        for point in segment.points:
            point_counter[point] += 1
    return point_counter


def solver(infile: str, no_diagonals: bool) -> int:
    """Solve part 1 and 2."""
    segments = read_input(infile)
    point_counter = count_overlaps(segments, no_diagonals=no_diagonals)
    over_1_points = [val for val in point_counter.values() if val >= 2]
    return len(over_1_points)


def part1(infile: str) -> int:
    """Solve part 1."""
    return solver(infile, no_diagonals=True)


def part2(infile: str) -> int:
    """Solve part 1."""
    return solver(infile, no_diagonals=False)


if __name__ == "__main__":
    eg1 = part1("example.txt")
    ega1 = 5
    if eg1 != ega1:
        raise ValueError(f"Example 1 got {eg1}, expected {ega1}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")

    eg2 = part2("example.txt")
    ega2 = 12
    if eg2 != ega2:
        raise ValueError(f"Example 2 got {eg2}, expected {ega2}")
    a2 = part2("input.txt")
    print(f"Part 2: {a2}")
