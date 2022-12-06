"""Tests for supply Stacks."""
import pytest

from advent_ipreston.year_2022.day06.puzzle import part1
from advent_ipreston.year_2022.day06.puzzle import part2


@pytest.mark.parametrize(
    "infile,result",
    [
        ("example1.txt", 5),
        ("example2.txt", 6),
        ("example3.txt", 10),
        ("example4.txt", 11),
    ],
)
def test_part01(infile: str, result: int) -> None:
    """Test part 1."""
    assert part1(infile) == result


@pytest.mark.parametrize(
    "infile,result",
    [
        ("example5.txt", 19),
        ("example6.txt", 23),
        ("example7.txt", 23),
        ("example8.txt", 29),
        ("example9.txt", 26),
    ],
)
def test_part02(infile: str, result: int) -> None:
    """Test part 1."""
    assert part2(infile) == result
