"""Day 17 of the advent of code challenge."""
from __future__ import annotations

from dataclasses import dataclass
import itertools
from pathlib import Path
from typing import Optional, Set


@dataclass(frozen=True)
class Vector:
    """I represent a vector in 3d integer space."""

    x: int
    y: int
    z: int
    w: Optional[int] = None


NEIGHBOUR_VECS = {
    Vector(*xyz)
    for xyz in itertools.product([1, 0, -1], repeat=3)
    if any(d != 0 for d in xyz)
}

NEIGHBOUR_VECS_4D = {
    Vector(*xyzw)
    for xyzw in itertools.product([1, 0, -1], repeat=4)
    if any(d != 0 for d in xyzw)
}


@dataclass(frozen=True)
class Cube:
    """I'm a conway cube."""

    x: int
    y: int
    z: int
    w: Optional[int] = None

    @property
    def neighbours(self) -> Set[Cube]:
        """Get all neighbour coordinates.

        MyPy doesn't like the optional w even though I know it's safe

        Returns
        -------
        Set[Cube]:
            All neighbour coordinates
        """
        cubes: Set[Cube]
        if self.w is None:
            cubes = {
                Cube(self.x + vec.x, self.y + vec.y, self.z + vec.z)
                for vec in NEIGHBOUR_VECS
            }
        else:
            cubes = {
                Cube(
                    self.x + vec.x,
                    self.y + vec.y,
                    self.z + vec.z,
                    self.w + vec.w,  # type: ignore
                )
                for vec in NEIGHBOUR_VECS_4D
            }
        return cubes


def read_inputs(filename: str, hypercube: bool = False) -> Set[Cube]:
    """Read in a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file, should be in the same folder as this module
    hypercube: bool
        Are we operating in 4D space?


    Returns
    -------
    Set[Cube]
        All the active cubes in the initial state
    """
    w: Optional[int]
    if hypercube:
        w = 0
    else:
        w = None
    here: Path = Path(__file__).resolve().parent
    in_path: Path = here / filename
    with open(in_path, "r") as f:
        return {
            Cube(x, y, 0, w)
            for y, line in enumerate(f.readlines())
            for x, char in enumerate(line)
            if char == "#"
        }


def cycle(current_active: Set[Cube]) -> Set[Cube]:
    """Run a cycle of the game of life, I mean energy source.

    Parameters
    ----------
    current_active: Set[Cube]
        All currently active cubes
    
    Returns
    -------
    Set[Cube]
        The new set of active cubes after one cycle
    """
    # start with an empty set, we'll add cubes as they match a rule
    new_active: Set[Cube] = set()
    # Handle the active cube rules
    for cube in current_active:
        active_neighbours: Set[Cube] = set.intersection(cube.neighbours, current_active)
        if 2 <= len(active_neighbours) <= 3:
            new_active.add(cube)
    # Handle the inactive cube rules
    # I think this is faster than checking for the intersection
    # of neighbours
    all_neighbours: Set[Cube] = set.union(*(cube.neighbours for cube in current_active))
    empty_neighbours: Set[Cube] = all_neighbours - current_active
    for cube in empty_neighbours:
        if len(cube.neighbours.intersection(current_active)) == 3:
            new_active.add(cube)
    return new_active


def part1(filename: str = "input.txt") -> int:
    """Solve part 1 of the challenge.

    Parameters
    ----------
    filename: str
        The name of the file, should be in the same folder as this module

    Returns
    -------
    int
        The answer to part 1
    """
    current_active: Set[Cube] = read_inputs(filename)
    for _ in range(6):
        current_active = cycle(current_active)
    return len(current_active)


def part2(filename: str = "input.txt") -> int:
    """Solve part 2 of the challenge.

    Parameters
    ----------
    filename: str
        The name of the file, should be in the same folder as this module

    Returns
    -------
    int
        The answer to part 2
    """
    current_active: Set[Cube] = read_inputs(filename, hypercube=True)
    for _ in range(6):
        current_active = cycle(current_active)
    return len(current_active)
