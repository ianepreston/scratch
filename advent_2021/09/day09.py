"""Advent of code 2021 day 9 puzzle."""
from typing import List, NamedTuple, Dict, Set
import math
from pathlib import Path


class Point(NamedTuple):
    x: int
    y: int


def gen_heightmap(infile: str) -> Dict[Point, int]:
    """Read in heightmap of the cave system."""
    inpath = Path(__file__).resolve().parent / infile
    heightmap = dict()
    with open(inpath, "r") as f:
        y = 0
        for line in f.readlines():
            for x, height in enumerate(int(c) for c in line.strip()):
                heightmap[Point(x, y)] = height
            y += 1
    return heightmap


class Cave:
    def __init__(self, infile: str) -> None:
        self.heightmap = gen_heightmap(infile)

    def find_adjacent_points(self, point: Point) -> List[Point]:
        """Get everywhere adjacent to a point."""
        adjacent_points = list()
        vecs = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for vec in vecs:
            xvec, yvec = vec
            adjx = point.x + xvec
            adjy = point.y + yvec
            adjp = Point(adjx, adjy)
            if adjp in self.heightmap.keys():
                adjacent_points.append(adjp)
        return adjacent_points

    def check_lowpoint(self, point: Point) -> bool:
        """Check if a point is a lowpoint."""
        adjacent_points = self.find_adjacent_points(point)
        pheight = self.heightmap[point]
        adjheight = min(self.heightmap[x] for x in adjacent_points)
        return pheight < adjheight

    def find_lowpoints(self) -> List[Point]:
        """Get all the lowpoints in the cave."""
        return [point for point in self.heightmap.keys() if self.check_lowpoint(point)]

    def p1(self) -> int:
        """Solve puzzle part 1."""
        return sum(self.heightmap[point] + 1 for point in self.find_lowpoints())

    def find_basin(self, lowpoint: Point) -> Set[Point]:
        """Find all the points that flow down to a lowpoint."""
        to_check = set([lowpoint])
        basin = set()
        while to_check:
            checkpoint = to_check.pop()
            checkheight = self.heightmap.get(checkpoint)
            if (checkheight is not None) and (checkheight < 9):
                basin.add(checkpoint)
                adjacents = self.find_adjacent_points(checkpoint)
                for adj in adjacents:
                    if adj not in basin:
                        to_check.add(adj)
        return basin

    def largest_basins(self) -> List[int]:
        basins = [self.find_basin(lowpoint) for lowpoint in self.find_lowpoints()]
        return sorted([len(basin) for basin in basins], reverse=True)[:3]

    def p2(self) -> int:
        return math.prod(self.largest_basins())


def part1(infile: str) -> int:
    """Solve part 1."""
    return Cave(infile).p1()


def part2(infile: str) -> int:
    """Solve part 2."""
    return Cave(infile).p2()


if __name__ == "__main__":
    eg1 = part1("example.txt")
    eg1a = 15
    if eg1 != eg1a:
        raise ValueError(f"Got {eg1}, expected {eg1a}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")
    eg2 = part2("example.txt")
    eg2a = 1134
    if eg2 != eg2a:
        raise ValueError(f"Got {eg2}, expected {eg2a}")
    a2 = part2("input.txt")
    print(f"Part 2: {a2}")
