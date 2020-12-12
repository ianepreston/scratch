"""Day 11 of the advent of code challenge."""
from __future__ import annotations

import itertools
from pathlib import Path
from typing import Dict, Iterable, List, NamedTuple, Tuple


def read_inputs(filename: str = "input.txt") -> List[Tuple[str, int]]:
    """Read in and parse a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    list[Tuple[str, int]]
        The directions
    """
    in_path: Path = Path(__file__).resolve().parent / filename
    with open(in_path, "r") as f:
        return [(line[0], int(line[1:])) for line in f.readlines()]


class Vector(NamedTuple):
    """Movement through 2D space."""

    x: int
    y: int


class Point(NamedTuple):
    """Location in 2D space."""

    x: int
    y: int


class Ship:
    """Sailing the friendly seas."""

    def __init__(self) -> None:
        """Start at 0,0 facing East."""
        self.location: Point = Point(0, 0)
        self.waypoint: Vector = Vector(10, 1)
        self.facing: str = "E"

    @staticmethod
    def _compass_to_vec(compass: str) -> Vector:
        """Turn NSEW into a vector.

        Parameters
        ----------
        compass: str
            N,S,E,orW

        Returns
        -------
        Vector
            The associated vector
        """
        compass_dict: Dict[str, Vector] = {
            "N": Vector(0, 1),
            "S": Vector(0, -1),
            "E": Vector(1, 0),
            "W": Vector(-1, 0),
        }
        if compass not in compass_dict:
            raise IndexError(f"{compass} is not a valid orientation")
        return compass_dict[compass]

    @property
    def manhattan_dist(self) -> int:
        """How far we got from where we started.

        Returns
        -------
        int
            The manhattan distance from 0,0
        """
        return abs(self.location.x) + abs(self.location.y)

    def rotate_ship(self, direction: str, degrees: int) -> None:
        """Turn the ship.

        Parameters
        ----------
        direction: str
            L or R
        degrees: int
            Multiple of 90 to turn
        """
        if direction not in ("L", "R"):
            raise ValueError(f"Invalid turn direction: {direction}")
        if degrees % 90 != 0:
            raise ValueError(f"Must turn multiple of 90 degrees, got {degrees}")
        num_turns: int = degrees // 90
        compass_seq_right: List[str] = ["N", "E", "S", "W"]
        compass_seq_left: List[str] = list(reversed(compass_seq_right))
        rotate_seq: Iterable[str]
        if direction == "R":
            rotate_seq = itertools.cycle(compass_seq_right)
        else:
            rotate_seq = itertools.cycle(compass_seq_left)
        # Get set up to our current direction
        new_dir: str = next(rotate_seq)
        while new_dir != self.facing:
            new_dir = next(rotate_seq)
        # Now turn the correct number of times
        for _ in range(num_turns):
            new_dir = next(rotate_seq)
        self.facing = new_dir

    def rotate_waypoint(self, direction: str, degrees: int) -> None:
        """Rotate the waypoint around the ship.

        https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python  # noqaB950

        Parameters
        ----------
        direction: str
            L or R
        degrees: int
            Multiple of 90 to turn
        """

        if direction not in ("L", "R"):
            raise ValueError(f"Invalid turn direction: {direction}")
        if direction == "R":
            if degrees == 90:
                self.waypoint = Vector(self.waypoint.y, -self.waypoint.x)
            elif degrees == 180:
                self.waypoint = Vector(-self.waypoint.x, -self.waypoint.y)
            elif degrees == 270:
                self.waypoint = Vector(-self.waypoint.y, self.waypoint.x)
        else:
            if degrees == 90:
                self.waypoint = Vector(-self.waypoint.y, self.waypoint.x)
            elif degrees == 180:
                self.waypoint = Vector(-self.waypoint.x, -self.waypoint.y)
            elif degrees == 270:
                self.waypoint = Vector(self.waypoint.y, -self.waypoint.x)

    def move(self, direction: str, amount: int, ship: bool = True) -> None:
        """Move the ship or waypoint.

        Parameters
        ----------
        direction: str
            Which way to move, N,S,E or W
        amount: int
            How far to move in that direction
        ship: bool
            Move the ship (default) or waypoint
        """
        vec: Vector = self._compass_to_vec(direction)
        scaled_vec: Vector = Vector(vec.x * amount, vec.y * amount)
        if ship:
            self.location = Point(
                self.location.x + scaled_vec.x, self.location.y + scaled_vec.y
            )
        else:
            self.waypoint = Vector(
                self.waypoint.x + scaled_vec.x, self.waypoint.y + scaled_vec.y
            )

    def move_to_waypoint(self, amount: int) -> None:
        """Move the ship in the direction of the waypoint.

        Parameters
        ----------
        amount: int
            Number of times to move along the waypoint vector
        """
        scaled_vec: Vector = Vector(self.waypoint.x * amount, self.waypoint.y * amount)
        self.location = Point(
            self.location.x + scaled_vec.x, self.location.y + scaled_vec.y
        )

    def take_direction_deprecated(self, direction: Tuple[str, int]) -> None:
        """Take a direction.

        Parameters
        ----------
        direction: Tuple[str, int]
            which way to move or turn and by how much
        """
        if direction[0] == "F":
            self.move(self.facing, direction[1])
        elif direction[0] in ("L", "R"):
            self.rotate_ship(*direction)
        elif direction[0] in ("N", "S", "E", "W"):
            self.move(*direction)
        else:
            raise ValueError(f"Invalid instruction f{direction}")

    def take_direction_updated(self, direction: Tuple[str, int]) -> None:
        """Take a direction using the new instructions.

        Parameters
        ----------
        direction: Tuple[str, int]
            which way to move or turn and by how much
        """
        if direction[0] == "F":
            self.move_to_waypoint(direction[1])
        elif direction[0] in ("L", "R"):
            self.rotate_waypoint(*direction)
        elif direction[0] in ("N", "S", "E", "W"):
            self.move(*direction, ship=False)
        else:
            raise ValueError(f"Invalid instruction f{direction}")


def part1(filename: str = "input.txt") -> int:
    """Solve part 1 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    int:
        The answer to part 1
    """
    directions: List[Tuple[str, int]] = read_inputs(filename)
    boaty_mc_boatface = Ship()
    for direction in directions:
        boaty_mc_boatface.take_direction_deprecated(direction)
    return boaty_mc_boatface.manhattan_dist


def part2(filename: str = "input.txt") -> int:
    """Solve part 2 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    int:
        The answer to part 2
    """
    directions: List[Tuple[str, int]] = read_inputs(filename)
    boaty_mc_boatface = Ship()
    for direction in directions:
        boaty_mc_boatface.take_direction_updated(direction)
    return boaty_mc_boatface.manhattan_dist


if __name__ == "__main__":
    part2("input.txt")
