"""Tests for Rock Paper Scissors."""
from advent_ipreston.year_2022.day02.puzzle import part1
from advent_ipreston.year_2022.day02.puzzle import part2


def test_part01() -> None:
    """Test part 1."""
    assert part1("example.txt") == 15


def test_part02() -> None:
    """Test part 1."""
    assert part2("example.txt") == 12
