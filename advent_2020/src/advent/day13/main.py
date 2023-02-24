"""Day 13 of the advent of code challenge."""
from __future__ import annotations

from pathlib import Path
from typing import List, NamedTuple, Tuple


def read_inputs(filename: str = "input.txt") -> Tuple[int, List[int]]:
    """Read in and parse a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    List[Tuple[int, List[int]]]
        Current time and bus list
    """
    in_path: Path = Path(__file__).resolve().parent / filename
    with open(in_path, "r") as f:
        current_time: int = int(f.readline())
        busses: List[int] = [
            int(char) for char in f.readline().split(",") if char != "x"
        ]
        return current_time, busses


class Bus(NamedTuple):
    """beep beep."""

    current_time: int
    frequency: int

    @property
    def minutes_to_next(self) -> int:
        """Calculate how many minutes until the next bus.

        Returns
        -------
        int:
            How many minutes until the next bus arrives
        """
        multiplier: int = (self.current_time // self.frequency) + 1
        minutes_left: int = (self.frequency * multiplier) - self.current_time
        return minutes_left

    @property
    def part1(self) -> int:
        """Answer part1 for a given bus.

        Returns
        -------
        int
            frequency * minutes_to_next
        """
        return self.frequency * self.minutes_to_next


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
    curr_time: int
    bus_nums: List[int]
    curr_time, bus_nums = read_inputs(filename)
    busses: List[Bus] = [Bus(curr_time, num) for num in bus_nums]
    next_bus: Bus = min(busses, key=lambda bus: bus.minutes_to_next)
    return next_bus.part1


class BusFreq(NamedTuple):
    """Bus 2 electric boogaloo."""

    period: int
    phase: int


def read_inputs2(filename: str = "input.txt") -> List[BusFreq]:
    """Read in and parse a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    List[int]
        Sum of ID and offset for each bus
    """
    in_path: Path = Path(__file__).resolve().parent / filename
    with open(in_path, "r") as f:
        _: str = f.readline()  # don't care about first line anymore
        return [
            BusFreq(int(x), i)
            for i, x in enumerate(f.readline().split(","))
            if x != "x"
        ]


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Compute Extended Greatest Common Divisor Algorithm.

    Parameters
    ----------
    a: int
        period of the first item
    b: int
        period of the second item

    Returns
    -------
    gcd: int
        The greatest common divisor of a and b.
    s, t: Tuple[int, int]
        Coefficients such that s*a + t*b = gcd

    Reference
    ---------
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def combine_phased_rotations(bus_a: BusFreq, bus_b: BusFreq) -> BusFreq:
    """Combine two phased rotations into a single phased rotation.

    Parameters
    ----------
    bus_a: BusFreq
        Phase and period of first bus
    bus_b: BusFreq
        Phase and period of the second bus

    Returns
    -------
    BusFreq
        The combined phase and period of the two input busses

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    gcd, s, t = extended_gcd(bus_a.period, bus_b.period)
    phase_difference = bus_a.phase - bus_b.phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")

    combined_period = bus_a.period // gcd * bus_b.period
    combined_phase = (bus_a.phase - s * pd_mult * bus_a.period) % combined_period
    return BusFreq(combined_period, combined_phase)


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

    Reference
    ---------
    https://math.stackexchange.com/questions/2218763/how-to-find-lcm-of-two-numbers-when-one-starts-with-an-offset  # noqaB950
    """
    busses: List[BusFreq] = read_inputs2(filename)
    current_bus: BusFreq = busses.pop()
    while busses:
        next_bus: BusFreq = busses.pop()
        current_bus = combine_phased_rotations(current_bus, next_bus)
    return -current_bus.phase % current_bus.period
