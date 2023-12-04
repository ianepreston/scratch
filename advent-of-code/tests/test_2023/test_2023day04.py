"""Tests for scratchards"""
from advent_ipreston.year_2023.day04.puzzle import part1
from advent_ipreston.year_2023.day04.puzzle import part2


def test_part01() -> None:
    """Test part 1."""
    assert part1("example.txt") == 13


def test_part02() -> None:
    """Test part 2."""
    assert part2("example.txt") == 30
