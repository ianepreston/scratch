"""Gear Ratios."""
from collections import defaultdict
from dataclasses import dataclass
from typing import List
from typing import Set

from advent_ipreston.helpers import inputs_generator


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    @property
    def adjacents(self) -> Set["Point"]:
        """Return the adjacent points."""
        possible = [
            Point(x=self.x, y=self.y + 1),
            Point(x=self.x + 1, y=self.y + 1),
            Point(x=self.x + 1, y=self.y),
            Point(x=self.x + 1, y=self.y - 1),
            Point(x=self.x, y=self.y - 1),
            Point(x=self.x - 1, y=self.y - 1),
            Point(x=self.x - 1, y=self.y),
            Point(x=self.x - 1, y=self.y + 1),
        ]
        return set(point for point in possible if (point.x >= 0 and point.y >= 0))


@dataclass
class Number:
    value: int
    points: Set[Point]


@dataclass
class Result:
    numbers: List[Number]
    symbols: Set[Point]


def parse_row(inrow: str, y: int, stars_only: bool = False) -> Result:
    """Parse a row."""
    numbers = list()
    symbols = set()
    current_number = []
    current_number_points = set()
    if stars_only:
        symbol_checker = lambda x: x == "*"
    else:
        symbol_checker = lambda x: x != "."
    for x, char in enumerate(inrow):
        if char.isdigit():
            current_number.append(char)
            current_number_points.add(Point(x=x, y=y))
        elif symbol_checker(char):
            symbols.add(Point(x=x, y=y))
        if current_number and not char.isdigit():
            numbers.append(
                Number(value=int("".join(current_number)), points=current_number_points)
            )
            current_number = []
            current_number_points = set()
    if current_number:
        numbers.append(
            Number(value=int("".join(current_number)), points=current_number_points)
        )
    return Result(numbers=numbers, symbols=symbols)


def parse_game(ingame: str, stars_only: bool = False) -> Result:
    """Parse a game."""
    numbers = list()
    symbols = set()
    for y, inrow in enumerate(inputs_generator(ingame)):
        row = parse_row(inrow=inrow, y=y, stars_only=stars_only)
        numbers.extend(row.numbers)
        symbols.update(row.symbols)
    return Result(numbers=numbers, symbols=symbols)


def part1(infile: str) -> int:
    """Solve part 1 of the puzzle."""
    game = parse_game(infile)
    value = 0
    for number in game.numbers:
        adjacents = set()
        for point in number.points:
            adjacents.update(point.adjacents)
        if adjacents.intersection(game.symbols):
            value += number.value
    return value


def part2(infile: str) -> int:
    """Solve part 2 of the puzzle."""
    game = parse_game(infile, stars_only=True)
    value = 0
    potential_gears = defaultdict(list)
    for gear in game.symbols:
        for number in game.numbers:
            adjacents = set(adj for point in number.points for adj in point.adjacents)
            if gear in adjacents:
                potential_gears[(gear.x, gear.y)].append(number.value)
                if len(potential_gears[(gear.x, gear.y)]) > 2:
                    break
    gears = {k: v for k, v in potential_gears.items() if len(v) == 2}
    for gear, values in gears.items():
        value += values[0] * values[1]
    return value


if __name__ == "__main__":  # pragma: no cover
    print(f"Part 1: {part1('puzzle.txt')}")
    print(f"Part 2: {part2('puzzle.txt')}")
