"""Advent of code 2021 day 6 puzzle."""
from pathlib import Path
from typing import List


def read_infile(infile: str) -> List[int]:
    inpath = Path(__file__).resolve().parent / infile
    with open(inpath, "r") as f:
        return [int(x) for x in f.readline().split(",")]


def breed_lanternfish(infile: str, days: int) -> int:
    """Get how many lanternfish we have after some time from a starting population."""
    countdowns = [0 for _ in range(9)]
    fish_in = read_infile(infile)
    for fish in fish_in:
        countdowns[fish] += 1
    for day in range(days):
        countdowns[(day + 7) % 9] += countdowns[day % 9]
    return sum(countdowns)


if __name__ == "__main__":
    days = 80
    eg1 = breed_lanternfish("example.txt", days)
    eg1a = 5934
    if eg1 != eg1a:
        raise ValueError(f"Example 1 got {eg1}, expected {eg1a}")
    a1 = breed_lanternfish("input.txt", days)
    print(f"Part 1: {a1}")
    days = 256
    eg2 = breed_lanternfish("example.txt", days)
    eg2a = 26984457539
    if eg2 != eg2a:
        raise ValueError(f"Example 2 got {eg2}, expected {eg2a}")
    a2 = breed_lanternfish("input.txt", days)
    print(f"Part 2: {a2}")
