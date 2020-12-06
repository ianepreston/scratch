"""Test examples and solutions to day 03."""
from advent.day06 import main


def test_part_1_example():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 11


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1()
    assert test_result == 6457


def test_part_2_example():
    """Check the example for part 2."""
    test_result = main.part2("example.txt")
    assert test_result == 6


def test_part_2_actual():
    """Check the example for part 2."""
    test_result = main.part2()
    assert test_result == 3260
