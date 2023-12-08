"""Tests for fertilizer."""
from advent_ipreston.year_2023.day05.puzzle import part1
from advent_ipreston.year_2023.day05.puzzle import part2


def test_part01() -> None:
    """Test part 1."""
    assert part1("example.txt") == 35


def test_part01solution() -> None:
    assert part1("puzzle.txt") == 31599214


def test_part02() -> None:
    """Test part 2."""
    assert part2("example.txt") == 46
