"""Tests for Calorie Counting."""
from advent_ipreston.year_2022.day01.puzzle import part1
from advent_ipreston.year_2022.day01.puzzle import part2


def test_part01() -> None:
    """Test part 1."""
    assert part1("example.txt") == 24_000


def test_part02() -> None:
    """Test part 1."""
    assert part2("example.txt") == 45_000
