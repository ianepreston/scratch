"""Day 24 of the advent of code challenge."""
from __future__ import annotations

from dataclasses import dataclass
import itertools
from pathlib import Path
from typing import Dict, List, NamedTuple


class Vector(NamedTuple):
    """Movement through 2D space."""

    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:  # type: ignore
        """Sum up vectors.

        Parameters
        ----------
        other: Vector
            The other vector to add to the first

        Returns
        -------
        Vector
            Sum of the two vectors
        """
        return Vector(self.x + other.x, self.y + other.y)


NEIGHBOUR_VECS = {
    Vector(*xy)
    for xy in itertools.product([1, 0, -1], repeat=2)
    if any(d != 0 for d in xy)
}


class Point(NamedTuple):
    """Location in 2D space."""

    x: int
    y: int

    def __add__(self, other: Vector) -> Point:  # type: ignore
        """Apply a vector to a point to find a new point.

        Parameters
        ----------
        other: Vector
            The other vector to add to the first

        Returns
        -------
        Point
            The new point after the vector is applied
        """
        return Point(self.x + other.x, self.y + other.y)


@dataclass
class Tile:
    """I'm a tile."""

    point: Point
    black: bool = False
    flips: int = 0

    def flip(self) -> bool:
        """Flip the tile.

        Returns
        -------
        bool:
            Whether the tile is black after the flip
        """
        self.black = not self.black
        self.flips += 1
        return self.black

    @property
    def neighbour_points(self) -> List[Point]:
        """List the location of the 6 adjacent tiles.

        Returns
        -------
        List[Point]
            The x,y coord of the 6 adjactent tiles
        """
        return [
            self.point + compass_to_vec(c) for c in ["nw", "ne", "sw", "se", "e", "w"]
        ]


def compass_to_vec(compass: str) -> Vector:
    """Turn NSEW into a vector.

    Parameters
    ----------
    compass: str
        nw, ne, sw, se, e, or w

    Returns
    -------
    Vector
        The associated vector
    """
    compass_dict: Dict[str, Vector] = {
        "nw": Vector(-1, 1),
        "ne": Vector(1, 1),
        "sw": Vector(-1, -1),
        "se": Vector(1, -1),
        "e": Vector(2, 0),
        "w": Vector(-2, 0),
    }
    if compass not in compass_dict:
        raise IndexError(f"{compass} is not a valid orientation")
    return compass_dict[compass]


def parse_line(line: str) -> Tile:
    """Read a line.

    Parameters
    ----------
    line: str
        The input line from the puzzle

    Returns
    -------
    Tile
        The tile you land on after taking all the steps.
    """
    tile_point = Point(0, 0)
    i = 0
    while i < len(line):
        if line[i] in ("n", "s"):
            c = "".join((line[i], line[i + 1]))
            i += 2
        else:
            c = line[i]
            i += 1
        tile_point += compass_to_vec(c)
    return Tile(tile_point)


def read_inputs(filename: str = "input.txt") -> List[Tile]:
    """Read in and parse a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    list[Tile]
        The tile positions
    """
    in_path: Path = Path(__file__).resolve().parent / filename
    with open(in_path, "r") as f:
        return [parse_line(line.strip()) for line in f.readlines()]


class Lobby:
    """I'm the floor of a hotel lobby."""

    def __init__(self, tile_dict: Dict[Point, Tile]) -> None:
        self.tile_dict = tile_dict
        self._add_neighbours()

    def _add_neighbours(self) -> None:
        """Make sure we have all relevant adjactent tiles included."""
        check_tiles = [tile for tile in self.tile_dict.values()]
        for tile in check_tiles:
            for neighbour in tile.neighbour_points:
                if neighbour not in self.tile_dict:
                    self.tile_dict[neighbour] = Tile(neighbour)

    def advance_day(self) -> None:
        """Do another conway style flip.

        Any black tile with zero or more than 2 black tiles immediately adjacent to it
        is flipped to white.

        Any white tile with exactly 2 black tiles immediately adjacent to it is flipped
        to black.
        """
        self._add_neighbours()

        def adjacent_blacks(tile: Tile) -> int:
            """How many of a tile's neighbours are black.

            Parameters
            ----------
            tile: Tile
                The tile to check

            Returns
            -------
            int: How many of that tile's neighbours are black
            """
            return sum(
                self.tile_dict[neighbour].black
                for neighbour in tile.neighbour_points
                if neighbour in self.tile_dict
            )

        def should_flip(tile: Tile) -> bool:
            """Check if a tile needs to flip.

            Parameters
            ----------
            tile: Tile
                The tile to check

            Returns
            -------
            bool
                If the tile needs to flip
            """
            adj_blk = adjacent_blacks(tile)
            if tile.black:
                return (adj_blk == 0) or (adj_blk > 2)
            else:
                return adj_blk == 2

        flip_points = [
            point
            for point in self.tile_dict.keys()
            if should_flip(self.tile_dict[point])
        ]
        for point in flip_points:
            self.tile_dict[point].flip()


def get_tile_dict(filename: str) -> Dict[Point, Tile]:
    """Read in the tiles.

    Parameters
    ----------
    filename: str
        The file to read in from this folder

    Returns
    -------
    Dict[Points, Tile]
        Dictionary of all the tiles read in and their flipped state
    """
    tiles = read_inputs(filename)
    tile_dict = dict()
    for tile in tiles:
        if tile.point not in tile_dict:
            tile_dict[tile.point] = tile
        tile_dict[tile.point].flip()
    return tile_dict


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
    tile_dict = get_tile_dict(filename)
    return sum(tile.black for tile in tile_dict.values())


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
    tile_dict = get_tile_dict(filename)
    lobby = Lobby(tile_dict)
    for _ in range(100):
        lobby.advance_day()
    return sum(tile.black for tile in lobby.tile_dict.values())
