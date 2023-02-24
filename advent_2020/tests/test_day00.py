"""Test examples and solutions to day 0 (2019 day 1)."""
import pytest

from advent.day00 import main


@pytest.mark.parametrize(
    "test_input,expected", [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
)
def test_part1_examples(test_input, expected):
    """Test example fuel calculations from part 1."""
    assert main.calc_fuel(test_input) == expected


def test_part1_actual():
    """Check the actual solution to part 1."""
    assert main.part1() == 3412496


@pytest.mark.parametrize("test_input,expected", [(14, 2), (1969, 966), (100756, 50346)])
def test_part2_examples(test_input, expected):
    """Check example fuel calculations from part 2."""
    assert main.recursive_fuel(test_input) == expected


def test_part2_actual():
    """Check the actual solution to part 2."""
    assert main.part2() == 5115845
