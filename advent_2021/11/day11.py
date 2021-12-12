"""Advent of code 2021 day 11 puzzle."""
from pathlib import Path
from typing import Dict, List, NamedTuple


class Coord(NamedTuple):
    row: int
    col: int


def parse_start_grid(infile: str) -> Dict[Coord, int]:
    """Get the starting grid for the puzzle."""
    inpath = Path(__file__).resolve().parent / infile
    row = 0
    start_grid = dict()
    with open(inpath, "r") as f:
        for line in f.readlines():
            for col, energystr in enumerate(line.strip()):
                coord = Coord(row, col)
                energy = int(energystr)
                start_grid[coord] = energy
            row += 1
    return start_grid


class OctoGrid:
    def __init__(self, infile: str) -> None:
        self.grid = parse_start_grid(infile)
        self.flashes = 0
        self.steps = 0

    def find_neighbors(self, coord: Coord) -> List[Coord]:
        """All points adjacent to a point."""
        vectors = (-1, 0, 1)
        neighbors = list()
        for rowvec in vectors:
            for colvec in vectors:
                if rowvec or colvec:
                    newrow = coord.row + rowvec
                    newcol = coord.col + colvec
                    newcoord = Coord(newrow, newcol)
                    if newcoord in self.grid.keys():
                        neighbors.append(newcoord)
        return neighbors

    def count_flashes(self) -> int:
        """How many octopi are flashing now."""
        return sum(x == 10 for x in self.grid.values())

    def reset_flashes(self) -> None:
        """Back to zero after flashing."""
        for key, value in self.grid.items():
            if value == 10:
                self.grid[key] = 0

    def increment(self):
        """Update energy on all your octopus friends."""
        to_increment = [key for key in self.grid.keys()]
        flashed_octos = set()
        while to_increment:
            coord = to_increment.pop(0)
            if self.grid[coord] < 10:
                self.grid[coord] += 1
            if (self.grid[coord] == 10) and (coord not in flashed_octos):
                reactions = [
                    x
                    for x in self.find_neighbors(coord)
                    if (self.grid[x] != 10) and (x not in flashed_octos)
                ]
                flashed_octos.add(coord)
                to_increment.extend(reactions)

    def step(self):
        """Step through the reactions."""
        self.steps += 1
        self.increment()
        self.flashes += self.count_flashes()
        self.reset_flashes()

    def find_synch_step(self) -> int:
        """Find when they all sync."""
        full_flash = len(self.grid)
        while True:
            last_flash = self.flashes
            self.step()
            next_flash = self.flashes
            if next_flash - last_flash == full_flash:
                return self.steps


def part1(infile: str) -> int:
    """Solve part 1."""
    octogrid = OctoGrid(infile)
    for _ in range(100):
        octogrid.step()
    return octogrid.flashes


def part2(infile: str) -> int:
    return OctoGrid(infile).find_synch_step()


if __name__ == "__main__":
    eg1 = part1("example.txt")
    eg1a = 1656
    if eg1 != eg1a:
        raise ValueError(f"Expected {eg1a}, got {eg1}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")
    eg2 = part2("example.txt")
    eg2a = 195
    if eg2 != eg2a:
        raise ValueError(f"Expected {eg2a}, got {eg2}")
    a2 = part2("input.txt")
    print(f"Part 2: {a2}")
