""""Day 01 for 2021 Advent of Code."""

from typing import List


EXAMPLE = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]


def input_to_list() -> List[int]:
    """Read the puzzle input as a list of integers."""
    with open("input.txt", "r") as f:
        return [int(line) for line in f.readlines()]


def naive_part1(sonar_readings: List[int]) -> int:
    """Count the number of times depth increased.

    Using a real basic solution and then might try fancier stuff with profiling later.
    """
    increased_count: int = 0
    for i in range(1, len(sonar_readings)):
        j = i - 1
        if sonar_readings[i] > sonar_readings[j]:
            increased_count += 1
    return increased_count


def naive_rolling_sum(sonar_readings: List[int]) -> List[int]:
    """Get a three entry rolling sum of sonar readings."""
    return [
        sum((sonar_readings[i - 2], sonar_readings[i - 1], sonar_readings[i]))
        for i in range(2, len(sonar_readings))
    ]


def naive_part2(sonar_readings: List[int]) -> int:
    """Count the number of times the rolling sum increased."""
    return naive_part1(naive_rolling_sum(sonar_readings))


if __name__ == "__main__":
    eg_part1 = naive_part1(EXAMPLE)
    if eg_part1 != 7:
        raise ValueError(f"Example part 1 should be 7, got {eg_part1}")
    part1 = naive_part1(input_to_list())
    print(f"Part 1: {part1}")
    eg_part2 = naive_part2(EXAMPLE)
    if eg_part2 != 5:
        raise ValueError(f"Example part 2 should be 5, got {eg_part2}")
    part2 = naive_part2(input_to_list())
    print(f"Part 2: {part2}")
