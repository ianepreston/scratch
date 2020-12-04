"""Test examples and solutions to day 03."""
from advent.day04 import main


def test_part_1_example():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 2


def test_part_1_actual():
    """Check the actual answer to part 1."""
    test_result = main.part1("input.txt")
    assert test_result == 254


def test_part_2_actual():
    """Check the actual answer to part 1."""
    test_result = main.part2("input.txt")
    assert test_result == 184
