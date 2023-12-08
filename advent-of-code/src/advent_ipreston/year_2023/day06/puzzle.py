"""Boat race"""
import math
from dataclasses import dataclass
from typing import List
from typing import Tuple

from advent_ipreston.helpers import inputs_generator


@dataclass
class Race:
    time_limit: int
    distance_record: int

    def _quadratic(self) -> Tuple[float, float]:
        """Solve the quadratic equation"""
        a = 1
        b = -self.time_limit
        c = self.distance_record
        x1 = (-b + (b**2 - 4 * a * c) ** 0.5) / (2 * a)
        x2 = (-b - (b**2 - 4 * a * c) ** 0.5) / (2 * a)
        return (x1, x2)

    @property
    def time_ranges(self) -> Tuple[int, int]:
        """Get the time ranges"""
        x1, x2 = self._quadratic()
        xmin = min(x1, x2)
        xmax = max(x1, x2)
        min_time = int(xmin) + 1
        if xmax % 1 == 0:
            max_time = int(xmax) - 1
        else:
            max_time = int(xmax)
        return (min_time, max_time)

    @property
    def winning_times(self) -> int:
        """Get the winning times"""
        min_time, max_time = self.time_ranges
        return max_time - min_time + 1


def parse_inputs_part1(instr: str) -> List[Race]:
    timestr, distancestr = (line for line in inputs_generator(instr))
    times = [int(time) for time in timestr.replace("Time: ", "").split()]
    distances = [
        int(distance) for distance in distancestr.replace("Distance: ", "").split()
    ]
    races = [Race(time, distance) for time, distance in zip(times, distances)]
    return races


def parse_inputs_part2(instr: str) -> Race:
    timestr, distancestr = (line for line in inputs_generator(instr))
    time = int("".join(timestr.replace("Time: ", "").split()))
    distance = int("".join(distancestr.replace("Distance: ", "").split()))
    return Race(time, distance)


def part1(instr: str) -> int:
    races = parse_inputs_part1(instr)
    return math.prod(race.winning_times for race in races)


def part2(instr: str) -> int:
    race = parse_inputs_part2(instr)
    return race.winning_times


if __name__ == "__main__":  # pragma: no cover
    print(f"Part 1: {part1('puzzle.txt')}")
    print(f"Part 2: {part2('puzzle.txt')}")
