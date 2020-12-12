"""Test examples and solutions to day 12."""
from advent.day12 import main


def test_part_1_example1():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 25


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1()
    assert test_result == 1565


def test_part_2_example1():
    """Check the example for part 2."""
    test_result = main.part2("example.txt")
    assert test_result == 286


def test_part_2_actual():
    """Check the example for part 2."""
    test_result = main.part2()
    assert test_result == 78883
